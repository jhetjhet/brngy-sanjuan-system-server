from django.core.files.base import File
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.core.paginator import Paginator
from rest_framework import (
    viewsets,
    mixins,
    permissions,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (
    Excel,
)
from .serializers import (
    ExcelSerializer,
)
from .dataframe_filters import (
    attribute_filter,
    columns_filter,
    ordering_filter,
    search_filter,
)

import pandas as pd
import numpy as np
import json
import re
from io import BytesIO

DATAFRAME_PAGINATION_SIZE = 20


class ExcelViewsets(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Excel.objects.all()
    serializer_class = ExcelSerializer
    # permission_classes = (
    #     permissions.IsAdminUser,
    # )

    @action(detail=False, methods=['GET'])
    def loaded(self, request, *args, **kwargs):
        latest_excel = self.get_queryset().order_by('-date_uploaded').first()
        if latest_excel:
            ser_data = ExcelSerializer(latest_excel).data
        return Response(status=200, data=(ser_data if latest_excel else None))

    @action(detail=True, methods=['GET'])
    def pivot(self, request, *args, **kwargs):
        excel = self.get_object()

        params = request.query_params
        index = params.get('index', None)
        values = params.get('values', None)
        columns = params.get('columns', None)
        aggfunc = params.get('aggfunc', 'count_nonzero')

        try:
            if not index and values:
                raise

            values = values.split(',')
            index = index.split(',')
            if columns:
                columns = columns.split(',')
            else:
                columns = []

            cencus = self.__get_cencus__(excel)
            piv_cencus = pd.pivot_table(
                cencus, index=index, values=values, columns=columns, aggfunc=getattr(np, aggfunc))

            return Response(status=200, data=json.loads(piv_cencus.to_json()))

        except:
            pass
        return Response(status=200)

    @action(detail=True, methods=['GET'])
    def filters(self, request, *args, **Kwargs):
        excel = self.get_object()

        params = request.query_params
        page = params.get('page', 1)

        cencus = self.__get_cencus__(excel)

        cencus = search_filter(cencus, params)
        cencus = ordering_filter(cencus, params)
        cencus = attribute_filter(cencus, params)
        cencus = columns_filter(cencus, params)

        cencus_paginator = Paginator(cencus, DATAFRAME_PAGINATION_SIZE)
        
        try:
            curr_page = cencus_paginator.page(page)
        except:
            curr_page = None

        return Response(status=200, data={
            'page': page,
            'count': cencus_paginator.count,
            'page_count': cencus_paginator.num_pages,
            'next_page': curr_page.next_page_number() if curr_page and curr_page.has_next() else None,
            'prev_page': curr_page.previous_page_number() if curr_page and curr_page.has_previous() else None,
            'results': json.loads(curr_page.object_list.to_json(orient='split')) if curr_page else {},
        })

    # process cacheing of cencus excel
    def __get_cencus__(self, excel):
        cencus = cache.get(excel.id)
        if type(cencus) != pd.DataFrame:
            cencus = pd.read_excel(excel.file.path)
            cache.set(excel.id, cencus, 180) # cache for 3mns
        return cencus
    
    def __replace_cencus__(self, excel, cencus):
        if cache.delete(excel.id):
            cache.set(excel.id, cencus, 180) # cache for 3mns
    
    def __update_excel_file__(self, excel, cencus):
        mem_cencus = BytesIO()
        cencus.to_excel(mem_cencus, index=False)
        cencus_file = File(mem_cencus)
        excel_file_name = excel.file.name

        # delete old excel file
        excel.file.delete(save=False)
        excel.file.save(excel_file_name, cencus_file)

    @action(detail=True, methods=['GET', 'PUT'], url_path=r'index/(?P<index>\d+)')
    def index(self, request, pk, index, *args, **Kwargs):
        excel = self.get_object()
        index = int(index)
        cencus = self.__get_cencus__(excel)

        def get_index_data(df, index):
            try:
                df = df.loc[int(index)]
                return json.loads(df.to_json())
            except:
                return {}

        if request.method == 'GET':
            return Response(data=get_index_data(cencus, index))

        elif request.method == 'PUT':
            data = request.data
            colmuns = set(cencus.columns).intersection(data.keys())

            if len(colmuns) > 1:

                cencus.at[index, colmuns] = [data[c] for c in colmuns]
                self.__replace_cencus__(excel, cencus)
                self.__update_excel_file__(excel, cencus)

                return Response(data=get_index_data(cencus, index))
        
        return Response()
    
    @action(detail=True, methods=['POST'], url_path=r'index')
    def add(self, request, pk, *args, **Kwargs):
        excel = self.get_object()
        cencus = self.__get_cencus__(excel)

        try:
            new_row = pd.DataFrame([request.data,])
            cencus = pd.concat([cencus, new_row], ignore_index=True)
            self.__replace_cencus__(excel, cencus)
            self.__update_excel_file__(excel, cencus)
        except:
            raise ValidationError('Invalid data format')

        return Response(data=request.data)