export interface CreateRequestParams {
  original_image: File
}

export interface RecordInfo {
  created_at: Date
  status: string
  detection_count: number
  processing_time: number
}
