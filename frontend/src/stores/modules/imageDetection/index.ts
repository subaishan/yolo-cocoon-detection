import { ref } from 'vue'
import { defineStore } from 'pinia'
import * as api from '@/api/imageDetection/index'
import * as types from './types'

export const useImageDetectionStore = defineStore('imageDetection', () => {
  //state
  const RecordID = ref<number[]>([])
  const RecordInfo = ref<Record<number, types.RecordInfo>>({})

  const getRecordID = () => {
    return RecordID.value
  }

  const getRecordInfo = () => {
    return RecordInfo.value
  }

  async function createRecord(params: types.CreateRequestParams) {
    try {
      const data = await api.Create(params)
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function recordList() {
    try {
      const data = await api.List()
      RecordID.value = data.results.map((item) => item.id)

      const infoDict: Record<number, types.RecordInfo> = {}
      data.results.forEach((item) => {
        infoDict[item.id] = {
          created_at: item.created_at,
          status: item.status,
          detection_count: item.detection_count,
          processing_time: item.processing_time,
        }
      })
      RecordInfo.value = infoDict

      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function recordDelete(id: number) {
    try {
      const data = await api.Delete(id)
      return data
    } catch (error) {
      console.log(error)
    }
  }

  async function recordRetrieve(id: number) {
    try {
      const data = await api.Retrieve(id)
      return data
    } catch (error) {
      console.log(error)
    }
  }

  return {
    getRecordID,
    getRecordInfo,
    createRecord,
    recordList,
    recordDelete,
    recordRetrieve,
  }
})
