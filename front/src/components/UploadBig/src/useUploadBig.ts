import {
  UploadBigDelItem,
  UploadBigItem,
  UploadBigMergeItem
} from '/@/api/demo/model/uploadBigModel';
import { defHttp } from '/@/utils/http/axios';
import { ErrorMessageMode } from '/#/axios';

enum Api {
  uploadBigFileUrl = '/upload/uploadfile',
  uploadBigMergeFileUrl = '/upload/mergefile',
  delBigUploadFileUrl = '/upload/removefile',
}

/**
 * @description: 上传大文件【分片】
 */
export function uploadBigFile(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<UploadBigItem>(
    {
      url: Api.uploadBigFileUrl,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}

/**
 * @description: 通知接口合并大文件【合并】
 */
export function uploadBigMergeFile(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<UploadBigMergeItem>(
    {
      url: Api.uploadBigMergeFileUrl,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}

/**
 * @description: 删除分片文件
 */
export function delBigUploadFile(params: {}, mode: ErrorMessageMode = 'modal') {
  //console.log(params);
  return defHttp.post<UploadBigDelItem>(
    {
      url: Api.delBigUploadFileUrl,
      params,
    },
    {
      errorMessageMode: mode,
      isReturnNativeResponse: true,
    },
  );
}
