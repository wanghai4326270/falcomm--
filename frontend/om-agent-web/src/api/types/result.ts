/** 与后端 `Result<T>` / `PageResult<T>` 对齐，供 Vben request 封装与页面消费 */
export interface Result<T> {
  code: number;
  message: string;
  data?: T;
}

export interface PageResult<T> {
  records: T[];
  total: number;
  page: number;
  pageSize: number;
}
