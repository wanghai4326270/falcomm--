package com.cn.om.complaint;

import com.cn.om.common.PageResult;
import com.cn.om.common.Result;
import com.cn.om.complaint.dto.ComplaintOrderRow;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 投诉工单查询（示例：青海 7 天）。真实权限由 Spring Security + 方法级注解控制，前端仅展示接口返回。
 */
@RestController
@RequestMapping("/api/v1/complaint/orders")
public class ComplaintOrderController {

    @GetMapping
    @PreAuthorize("hasAuthority('complaint:query')")
    public Result<PageResult<ComplaintOrderRow>> list(
            @RequestParam String provinceCode,
            @RequestParam int days) {
        List<ComplaintOrderRow> rows = List.of(
                sample(1L, "QH-063-250401-00001", "139****9733", "漫游地数据无法激活，多次拨测失败", "2025-04-08 09:12:33", 3),
                sample(2L, "QH-063-250407-00015", "136****8818", "语音主叫单通，被叫侧无声", "2025-04-07 14:22:01", 5),
                sample(3L, "QH-063-250405-00008", "155****1200", "物联网卡上网速率不达标", "2025-04-05 11:05:44", 2)
        );
        PageResult<ComplaintOrderRow> page = new PageResult<>(rows, rows.size(), 1, 20);
        return Result.ok(page);
    }

    private static ComplaintOrderRow sample(Long id, String orderNo, String msisdn, String content, String createdAt, int step) {
        ComplaintOrderRow r = new ComplaintOrderRow();
        r.setId(id);
        r.setOrderNo(orderNo);
        r.setMsisdnMasked(msisdn);
        r.setContent(content);
        r.setCreatedAt(createdAt);
        r.setCurrentStepIndex(step);
        return r;
    }
}
