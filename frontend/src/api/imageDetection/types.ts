export interface CreateRequestParams {
  original_image: File
}

// 检测框数据类型
export interface DetectionData {
  class_id: number
  class_name: string
  confidence: number
  bbox: [number, number, number, number] // [x1, y1, x2, y2]
  area: number
}

// 检测结果数据类型
export interface DetectionResult {
  detection_data: DetectionData[]
  detection_count: number
  processing_time: number
}

// API响应类型
export interface CreateResponseParams {
  success: boolean
  data: DetectionResult
  image: string
}

export interface ListResponseParams {
  count: number
  next: string
  previous: string
  results: {
    id: number
    created_at: Date
    status: string
    detection_count: number
    processing_time: number
  }[]
}

export interface RetrieveResponseParams {
  original_image: string
  processed_image: string
  detection_data: DetectionData[]
}
