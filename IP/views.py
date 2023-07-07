from rest_framework.viewsets import ModelViewSet
from IP.models import IpInfo, RegGatherInfo, SingleRegInfo, ValueInfo, FilesModel, TemplateFilesModel, CategoryInfo, \
    modificationInfo, IpPageFilesModel
from IP.sers import IpSerializers, RegGatherSerializers, SingleRegSerializers, ValueSerializers, FilesSerializer, \
    TemplateFilesSerializer, CategorySerializers, modificationSerializer, IpPageFilesSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from User.models import UserInfo
import docx
import uuid
import os, json
from django.http import FileResponse
from django.utils import timezone
import pandas as pd


# Create your views here.

class IpView(ModelViewSet):
    """IP视图"""
    queryset = IpInfo.objects.all()
    serializer_class = IpSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_ = ('ip_uuid', 'category', 'version', 'child_version', 'ip_name', 'private_project')  # 指定可搜索的字段
    filterset_fields = ('ip_uuid', 'category', 'version', 'child_version', 'ip_name', 'private_project')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('ip_uuid'))
        queryset = IpInfo.objects.filter(ip_uuid=request.GET.get('ip_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = IpInfo.objects.get(ip_uuid=request.GET.get('ip_uuid'))
        serializer = IpSerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        # data = request.data
        # if 'private_project' in data:
        #     # 在数据库中查询是否存在相同的记录
        #     if not data.get('private_project'):
        #         exists = IpInfo.objects.filter(ip_name=data.get('ip_name'), category=data.get('category'),
        #                                        version=data.get('child_version')).exists()
        #         if exists:
        #             return Response({'error': '子版本已存在'})
        #         else:
        #             serializer = IpSerializers(data=request.data, instance=queryset)
        #             if serializer.is_valid():
        #                 serializer.save()
        #                 return Response(serializer.data)
        #             else:
        #                 return Response(serializer.errors)
        #     else:
        #         exists = IpInfo.objects.filter(ip_name=data.get('ip_name'), category=data.get('category'),
        #                                        version=data.get('version')).exists()
        #         if exists:
        #             return Response({'error': '版本已存在'})
        #         else:
        #             serializer = IpSerializers(data=request.data, instance=queryset)
        #             if serializer.is_valid():
        #                 serializer.save()
        #                 return Response(serializer.data)
        #             else:
        #                 return Response(serializer.errors)

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'private_project' in data:
            # 在数据库中查询是否存在相同的记录
            if data.get('private_project') == "false":
                exists = IpInfo.objects.filter(version=data.get('version'), ip_name=data.get('ip_name'),
                                               category=data.get('category')).exists()
                if exists:
                    return Response({'error': '版本已存在'})
            else:
                exists = IpInfo.objects.filter(version=data.get('version'), child_version=data.get('child_version'),
                                               ip_name=data.get('ip_name'), category=data.get('category')).exists()
                if exists:
                    return Response({'error': '子版本已存在'})

        return super().create(request, *args, **kwargs)


class RegGatherView(ModelViewSet):
    """RegGather视图"""
    queryset = RegGatherInfo.objects.all()
    serializer_class = RegGatherSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('ip_uuid', 'tag', 'reg_gather_name', 'reg_gather_uuid')  # 指定可搜索的字段
    filterset_fields = ('ip_uuid', 'tag', 'reg_gather_name', 'reg_gather_uuid')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('reg_gather_uuid'))
        queryset = RegGatherInfo.objects.filter(reg_gather_uuid=request.GET.get('reg_gather_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = RegGatherInfo.objects.get(reg_gather_uuid=request.GET.get('reg_gather_uuid'))
        # print("queryset",queryset.reset)
        # print(request.data["reset"])
        if queryset.reg_gather_name != request.data["reg_gather_name"] \
                or queryset.tag != request.data["tag"] \
                or queryset.offset != request.data["offset"] \
                or queryset.description != request.data["description"] \
                or queryset.reset != request.data["reset"] \
                or queryset.address != request.data["address"] \
                or queryset.reg_ram != request.data["reg_ram"] \
                or queryset.retention != request.data["retention"]:

            temp_former_content = json.dumps(
                {'reg_gather_name': queryset.reg_gather_name,
                 'reg_gather_uuid': queryset.reg_gather_uuid,
                 'offset': queryset.offset,
                 'description': queryset.description,
                 'reset': queryset.reset,
                 'tag': queryset.tag}, )
            serializer = RegGatherSerializers(data=request.data, instance=queryset)
            if serializer.is_valid():
                if request.META.get('HTTP_AUTHORIZATION'):
                    serializer.save()
                    user = request.META.get('HTTP_AUTHORIZATION').split(",")[0]
                    user_uuid = request.META.get('HTTP_AUTHORIZATION').split(",")[1]
                    modificationInfo.objects.create(user=user,
                                                    user_uuid=UserInfo.objects.get(user_uuid=user_uuid),
                                                    data=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    former_content=temp_former_content,
                                                    modify_content=json.dumps(request.data),
                                                    modify_model="RegGather",
                                                    )
                else:
                    return Response("请登陆后在修改")
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("不需要修改")


class SingleRegView(ModelViewSet):
    """SingleReg视图"""
    queryset = SingleRegInfo.objects.all()
    serializer_class = SingleRegSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('reg_gather_uuid', 'single_reg_uuid')  # 指定可搜索的字段
    filterset_fields = ('reg_gather_uuid', 'single_reg_uuid')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        queryset = SingleRegInfo.objects.filter(single_reg_uuid=request.GET.get('single_reg_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = SingleRegInfo.objects.get(single_reg_uuid=request.GET.get('single_reg_uuid'))
        if queryset.start_bit != request.data["start_bit"] \
                or queryset.end_bit != request.data["end_bit"] \
                or queryset.RW != request.data["RW"] \
                or queryset.field != request.data["field"] \
                or queryset.note != request.data["note"] \
                or queryset.description != request.data["description"] \
                or queryset.reset_value != request.data["reset_value"] \
                or queryset.hw_RW != request.data["hw_RW"]:
            temp_former_content = json.dumps(
                {'single_reg_uuid': queryset.single_reg_uuid,
                 'reg_gather_uuid': queryset.reg_gather_uuid_id,
                 'start_bit': queryset.start_bit,
                 'end_bit': queryset.end_bit,
                 'RW': queryset.RW,
                 'field': queryset.field,
                 'note': queryset.note,
                 'description': queryset.description,
                 'reset_value': queryset.reset_value}, )
            serializer = SingleRegSerializers(data=request.data, instance=queryset)
            if serializer.is_valid():
                if request.META.get('HTTP_AUTHORIZATION'):
                    user = request.META.get('HTTP_AUTHORIZATION').split(",")[0]
                    user_uuid = request.META.get('HTTP_AUTHORIZATION').split(",")[1]
                    serializer.save()
                    modificationInfo.objects.create(user=user,
                                                    user_uuid=UserInfo.objects.get(user_uuid=user_uuid),
                                                    data=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    former_content=temp_former_content,
                                                    modify_content=json.dumps(request.data),
                                                    modify_model="SingleReg",
                                                    )

                    return Response(serializer.data)
                else:
                    return Response("请登陆后在修改")

            else:
                return Response(serializer.errors)
        else:
            return Response("不需要修改")

    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     if int(data.get('start_bit')) > 30:
    #         return Response({'error': 'start_bit must be less than 30'})
    #     if int(data.get('end_bit')) > 31:
    #         return Response({'error': 'end_bit must be less than 31'})
    #     if int(data.get('end_bit')) < int(data.get('start_bit')):
    #         return Response({'error': 'end_bit must be greater than start_bit'})
    #     if data.get('RW') not in ["R", "r", "W", "w", "r/w", "R/W"]:
    #         return Response({'error': 'RW must be R or RW or W'})
    #     return super().create(request, *args, **kwargs)


class ValueView(ModelViewSet):
    """Value视图"""
    queryset = ValueInfo.objects.all()
    serializer_class = ValueSerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('single_reg_uuid', 'id')  # 指定可搜索的字段
    filterset_fields = ('single_reg_uuid', 'id')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('value_uuid'))
        queryset = ValueInfo.objects.filter(value_uuid=request.GET.get('value_uuid')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = ValueInfo.objects.get(value_uuid=request.GET.get('value_uuid'))
        if queryset.value != request.data["value"] \
                or queryset.valueId != request.data["valueId"] \
                or queryset.description != request.data["description"]:
            # print(queryset.value, request.data["value"])
            # print(queryset.valueId, request.data["valueId"])
            # print(queryset.description, request.data["description"])
            # if request.data["description"] is None:
            #     print(request.data["description"])
            #     request.data["description"] = None
            temp_former_content = json.dumps(
                {'single_reg_uuid': queryset.single_reg_uuid_id,
                 'value_uuid': queryset.value_uuid,
                 'value': queryset.value,
                 'valueId': queryset.valueId,
                 'description': queryset.description})

            serializer = ValueSerializers(data=request.data, instance=queryset)
            if serializer.is_valid():
                if request.META.get('HTTP_AUTHORIZATION'):
                    serializer.save()
                    user = request.META.get('HTTP_AUTHORIZATION').split(",")[0]
                    user_uuid = request.META.get('HTTP_AUTHORIZATION').split(",")[1]
                    modificationInfo.objects.create(user=user,
                                                    user_uuid=UserInfo.objects.get(user_uuid=user_uuid),
                                                    data=timezone.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                    former_content=temp_former_content,
                                                    modify_content=json.dumps(request.data),
                                                    modify_model="Value",
                                                    )
                else:
                    return Response("请登陆后在修改")
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

        else:
            return Response("不需要修改")


class CategoryView(ModelViewSet):
    """种类视图"""
    queryset = CategoryInfo.objects.all()
    serializer_class = CategorySerializers
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器

    # search_fields = 'category'  # 指定可搜索的字段
    # filterset_fields = 'category'

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        # print(request.GET.get('value_uuid'))
        queryset = CategoryInfo.objects.filter(category=request.GET.get('category')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=False)
    def put(self, request):
        queryset = CategoryInfo.objects.get(id=request.data['id'])
        serializer = CategorySerializers(data=request.data, instance=queryset)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def create(self, request, *args, **kwargs):
        data = request.data
        exists = CategoryInfo.objects.filter(category=data.get('category')).exists()
        if exists:
            return Response({'error': '种类已存在'})
        return super().create(request, *args, **kwargs)


class FileViewSet(ModelViewSet):
    """导入spec文件视图"""
    queryset = FilesModel.objects.all()
    serializer_class = FilesSerializer

    # @api_view(['POST'])
    # def file_upload_view(self,request):
    #     serializer = FilesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         file = serializer.validated_data['file']
    #         # 处理文件逻辑
    #         print(file)
    #         return Response({'message': '文件上传成功'})
    #     else:
    #         return Response(serializer.errors, status=400)

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file is not None:
            serializer = FilesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            # 在这里处理上传的文件，例如保存到服务器或对文件进行其他操作
            reloadData(file, request.data.get('ip_uuid'))
            return Response({'message': 'File uploaded successfully'})
        else:
            return Response({'message': 'No file uploaded'}, status=400)


def find_index(dictionary_list, key, value):
    for index, item in enumerate(dictionary_list):
        if item.get(key) == value:
            return index
    return -1


def reloadData(file_name, file_ip_uuid):
    if file_name.name.split(".")[1] == "doc" or file_name.name.split(".")[1] == "docx":
        # 定义表格索引
        table_index = 0
        # 打开Word文档
        document = docx.Document(file_name)
        # 遍历文档中的所有表格
        for table in document.tables:
            # 打印表格索引
            # print(f'Table {table_index}:')

            # 遍历表格中的所有行
            gather_obj = {}
            single_reg_obj = {}
            for i, row in enumerate(table.rows):
                # 定义行索引和数据列表
                row_index = i
                data = []
                # 定义一个空list用于存放去重后的元素
                new_list = []

                # 遍历行中的所有单元格
                for j, cell in enumerate(row.cells):
                    # 定义列索引和单元格文本
                    col_index = j
                    cell_text = cell.text
                    # 将单元格文本添加到数据列表中
                    data.append(cell_text)

                # 打印行索引和数据列表
                # 遍历原list中的元素
                for element in data:
                    new_list.append(element)
                    # 判断当前元素是否已经存在于new_list中
                    # if element not in new_list:
                    #     # 如果不存在，则将其添加到new_list中
                    #     new_list.append(element)

                if table_index != 0:
                    if row_index == 0:
                        gather_obj["ip_uuid"] = file_ip_uuid
                        gather_obj["reg_gather_uuid"] = str(uuid.uuid4())
                        gather_obj["reg_gather_name"] = new_list[0]
                        gather_obj["offset"] = new_list[2]
                        gather_obj["single_reg_list"] = []
                    elif row_index == 1:
                        gather_obj["reset"] = new_list[0]
                    elif row_index == 2:
                        gather_obj["description"] = new_list[0]
                    elif row_index > 3:
                        if "/" not in new_list:
                            single_reg_obj["single_reg_uuid"] = str(uuid.uuid4())
                            single_reg_obj["reg_gather_uuid"] = gather_obj["reg_gather_uuid"]
                            if ":" not in new_list[0]:
                                single_reg_obj["start_bit"] = new_list[0]
                                single_reg_obj["end_bit"] = new_list[0]
                            else:
                                single_reg_obj["start_bit"] = new_list[0].split(":")[0]
                                single_reg_obj["end_bit"] = new_list[0].split(":")[1]
                            single_reg_obj["reset_value"] = new_list[1]
                            single_reg_obj["RW"] = new_list[2]
                            single_reg_obj["field"] = new_list[3]
                            single_reg_obj["value_list"] = []
                            if len(gather_obj["single_reg_list"]) > 0:
                                has_obj = find_index(gather_obj["single_reg_list"], "start_bit",
                                                     single_reg_obj["start_bit"])
                                if has_obj != -1:
                                    value_obj = {"des": new_list[-1]}
                                    gather_obj["single_reg_list"][has_obj]["value_list"].append(value_obj)
                                    # gather_obj["single_reg_list"][has_obj]["des"] = new_list[-1]
                                else:
                                    gather_obj["single_reg_list"].append(single_reg_obj)
                            else:
                                gather_obj["single_reg_list"].append(single_reg_obj)
                            single_reg_obj = {}
                # print(f'  Row {row_index}: {new_list}')
            if gather_obj:
                RegGatherInfo.objects.create(ip_uuid=IpInfo.objects.get(ip_uuid=file_ip_uuid),
                                             reg_gather_uuid=gather_obj['reg_gather_uuid'],
                                             offset=gather_obj['offset'],
                                             tag='draft',
                                             reg_gather_name=gather_obj['reg_gather_name'])
                if len(gather_obj['single_reg_list']) > 0:
                    # des,value_uuid,single_reg_uuid
                    for item in gather_obj['single_reg_list']:
                        SingleRegInfo.objects.create(
                            single_reg_uuid=item['single_reg_uuid'],
                            reg_gather_uuid=RegGatherInfo.objects.get(reg_gather_uuid=item['reg_gather_uuid']),
                            start_bit=item['start_bit'],
                            end_bit=item['end_bit'],
                            reset_value=item['reset_value'],
                            RW=item['RW'],
                            field=item['field'],
                        )
                        if len(item["value_list"]) > 0:
                            for value in item["value_list"]:
                                ValueInfo.objects.create(
                                    value="0",
                                    value_uuid=str(uuid.uuid4()),
                                    single_reg_uuid=SingleRegInfo.objects.get(single_reg_uuid=item['single_reg_uuid']),
                                    description=value["des"]
                                )
            # 增加表格索引
            table_index += 1
    elif file_name.name.split(".")[1] == "xls" or file_name.name.split(".")[1] == "xlsx":
        xl = pd.ExcelFile(file_name, engine='openpyxl')
        for name in xl.sheet_names:
            data = pd.read_excel(xl, name, header=1, keep_default_na=False)
            reg_gather_uuid = str(uuid.uuid4())
            for index, row in data.iterrows():
                gather_obj = {}
                single_reg_obj = {}
                for column in data.columns:
                    # print(column,row[column])
                    if row['Reg Name']:
                        gather_obj["ip_uuid"] = file_ip_uuid
                        reg_gather_uuid = str(uuid.uuid4())
                        gather_obj["reg_gather_uuid"] = reg_gather_uuid
                        gather_obj[column] = row[column]
                    if row['Sub Reg Name']:
                        single_reg_obj["single_reg_uuid"] = str(uuid.uuid4())
                        single_reg_obj["reg_gather_uuid"] = reg_gather_uuid
                        if column == 'Bit Width':
                            if isinstance(row[column], str) and ":" in row[column]:
                                single_reg_obj["start_bit"] = row[column].split(":")[0]
                                single_reg_obj["end_bit"] = row[column].split(":")[1]
                            else:
                                single_reg_obj["start_bit"] = row[column]
                                single_reg_obj["end_bit"] = row[column]
                        single_reg_obj[column] = row[column]
                if gather_obj:
                    # print(gather_obj)
                    RegGatherInfo.objects.create(ip_uuid=IpInfo.objects.get(ip_uuid=file_ip_uuid),
                                                 reg_gather_uuid=gather_obj['reg_gather_uuid'],
                                                 offset=gather_obj['Offset Addr'],
                                                 tag='draft',
                                                 reg_gather_name=gather_obj['Reg Name'],
                                                 address=gather_obj['Addr'],
                                                 reg_ram=gather_obj['reg/ram'],
                                                 retention=gather_obj['Retention'],
                                                 )
                if single_reg_obj:
                    # print(single_reg_obj)
                    SingleRegInfo.objects.create(
                        single_reg_uuid=single_reg_obj['single_reg_uuid'],
                        reg_gather_uuid=RegGatherInfo.objects.get(reg_gather_uuid=single_reg_obj['reg_gather_uuid']),
                        start_bit=single_reg_obj['start_bit'],
                        end_bit=single_reg_obj['end_bit'],
                        reset_value=single_reg_obj['Default Value'],
                        RW=single_reg_obj['Soft R/W'],
                        field=single_reg_obj['Sub Reg Name'],
                        description=single_reg_obj['Describe'],
                        hw_RW=single_reg_obj['HW R/W']
                    )


class TemplateFileViewSet(ModelViewSet):
    """导入spec文件视图"""
    queryset = TemplateFilesModel.objects.all()
    serializer_class = TemplateFilesSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('id', 'name', 'file_uuid')  # 指定可搜索的字段
    filterset_fields = ('id', 'name', 'file_uuid')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        queryset = TemplateFilesModel.objects.filter(file_uuid=request.GET.get('file_uuid'))
        # queryset = TemplateFilesModel.objects.filter(id=request.GET.get('id')).delete()
        # print(queryset.values('file')[0]['file'])
        if delete_file(queryset.values('file')[0]['file']):
            queryset.delete()
            return Response({'message': '文件删除成功'})
        else:
            return Response({'message': '文件删除失败'})
        # queryset
        # return Response(status=status.HTTP_204_NO_CONTENT)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def download_docx(request, *args, **kwargs):
    if request.path == "/api/ip/download_spec/":
        queryset = TemplateFilesModel.objects.filter(file_uuid=request.GET.get('file_uuid'))
    else:
        queryset = IpPageFilesModel.objects.filter(file_uuid=request.GET.get('file_uuid'))
    filename = queryset.values('file')[0]['file']
    # 检查文件是否存在
    if not os.path.exists(filename):
        # 如果文件不存在，返回适当的错误响应
        return Response(status=404)

    # 通过FileResponse发送文件响应

    response = FileResponse(open(filename, 'rb'),
                            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename="your-docx-file.docx"'
    return response


class modificationInfoView(ModelViewSet):
    """操作记录视图"""
    queryset = modificationInfo.objects.all()
    serializer_class = modificationSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)


class IpPageFilesViewSet(ModelViewSet):
    """导入spec头文件视图"""
    queryset = IpPageFilesModel.objects.all()
    serializer_class = IpPageFilesSerializer
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # 指定过滤器
    search_fields = ('name', 'version', 'create_user', 'upload_data', 'file_uuid', 'ip_uuid')
    # 指定可搜索的字段
    filterset_fields = ('name', 'version', 'create_user', 'upload_data', 'file_uuid', 'ip_uuid')

    @action(methods=['delete'], detail=False)
    def delete(self, request):
        queryset = IpPageFilesModel.objects.filter(file_uuid=request.GET.get('file_uuid'))
        # queryset = TemplateFilesModel.objects.filter(id=request.GET.get('id')).delete()
        # print(queryset.values('file')[0]['file'])
        if delete_file(queryset.values('file')[0]['file']):
            queryset.delete()
            return Response({'message': '文件删除成功'})
        else:
            return Response({'message': '文件删除失败'})

    def create(self, request, *args, **kwargs):
        ip_page_file = request.FILES.get('file')
        if ip_page_file is not None:
            serializer = IpPageFilesSerializer(data=request.data)
            # 检查数据是否存在
            if serializer.is_valid():
                serializer.save()
            # 在这里处理上传的文件，例如保存到服务器或对文件进行其他操作
            return Response({'message': '文件上传成功'})

        else:
            return Response({'message': 'No file uploaded'}, status=400)