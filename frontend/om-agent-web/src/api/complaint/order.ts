import type { Result, PageResult } from '@/api/types/result';

export interface ComplaintOrderRow {
  id: number;
  orderNo: string;
  msisdnMasked: string;
  content: string;
  createdAt: string;
  currentStepIndex: number;
}

/** 对接 GET /api/v1/complaint/orders（需携带 Basic 或后续 JWT） */
export async function fetchComplaintOrders(provinceCode: string, days: number) {
  const q = new URLSearchParams({ provinceCode, days: String(days) });
  const res = await fetch(`/api/v1/complaint/orders?${q.toString()}`, {
    credentials: 'include',
    headers: {
      Authorization: 'Basic ' + btoa('ops:ops'),
    },
  });
  const body = (await res.json()) as Result<PageResult<ComplaintOrderRow>>;
  if (!res.ok || body.code !== 0) {
    throw new Error(body.message || res.statusText);
  }
  return body;
}
