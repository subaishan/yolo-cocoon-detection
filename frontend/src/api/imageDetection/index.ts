import request from '@/api/request'
import { IMAGEDETECTION_API } from '../constants'
import * as Types from './types'

export const Create = (data: Types.CreateRequestParams): Promise<Types.CreateResponseParams> => {
  return request.post(IMAGEDETECTION_API.CREATE, data)
}

export const List = (): Promise<Types.ListResponseParams> => {
  return request.get(IMAGEDETECTION_API.LIST)
}

export const Delete = (id: number) => {
  return request.delete(`${IMAGEDETECTION_API.DELETE}${id}/`)
}

export const Retrieve = (id: number): Promise<Types.RetrieveResponseParams> => {
  return request.get(`${IMAGEDETECTION_API.RETRIEVE}${id}/`)
}
