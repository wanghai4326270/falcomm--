package com.cn.om.complaint.dto;

/**
 * 投诉工单列表行（与前端表格字段对齐）。
 */
public class ComplaintOrderRow {

    private Long id;
    private String orderNo;
    private String msisdnMasked;
    private String content;
    private String createdAt;
    /** 当前环节索引 0-5：自动接单…闭环确认 */
    private int currentStepIndex;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getOrderNo() {
        return orderNo;
    }

    public void setOrderNo(String orderNo) {
        this.orderNo = orderNo;
    }

    public String getMsisdnMasked() {
        return msisdnMasked;
    }

    public void setMsisdnMasked(String msisdnMasked) {
        this.msisdnMasked = msisdnMasked;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(String createdAt) {
        this.createdAt = createdAt;
    }

    public int getCurrentStepIndex() {
        return currentStepIndex;
    }

    public void setCurrentStepIndex(int currentStepIndex) {
        this.currentStepIndex = currentStepIndex;
    }
}
