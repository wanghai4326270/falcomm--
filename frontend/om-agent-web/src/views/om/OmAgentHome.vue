<template>
  <a-layout class="min-h-screen bg-[#f7f8fa]">
    <a-layout-sider width="260" theme="light" class="border-r border-gray-200 !overflow-auto" style="position: relative">
      <div class="p-4 border-b border-gray-200">
        <div class="flex items-center gap-2 mb-4">
          <a-avatar class="!bg-gradient-to-br from-blue-500 to-indigo-600">核</a-avatar>
          <span class="font-semibold text-gray-900">核心网运维智能体</span>
        </div>
        <a-button type="primary" block class="rounded-xl" @click="resetHome">新对话</a-button>
      </div>
      <div class="p-3 pb-20">
        <div class="text-xs text-gray-500 mb-2">历史对话</div>
        <a-list size="small" :data-source="history" :bordered="false">
          <template #renderItem="{ item }">
            <a-list-item class="!px-2 rounded-lg hover:bg-gray-100 cursor-pointer">{{ item }}</a-list-item>
          </template>
        </a-list>
      </div>
      <div class="absolute bottom-0 left-0 right-0 p-3 text-xs text-gray-500 border-t border-gray-200 bg-white">
        用户 运维账号
      </div>
    </a-layout-sider>

    <a-layout class="!min-h-screen">
      <a-layout-header class="!h-auto !leading-none py-3 px-6 bg-white/90 border-b border-gray-200 flex justify-between items-center">
        <span class="text-xs text-gray-500">{{ headerLabel }} | 内容由模型 AI 生成</span>
        <a-button type="link" size="small">退出登录</a-button>
      </a-layout-header>

      <a-layout-content v-if="view === 'home'" class="overflow-auto p-6" style="padding-bottom: 140px">
        <div class="max-w-3xl mx-auto text-center mt-16 mb-10">
          <h1 class="text-2xl font-semibold text-gray-900">有什么我能帮你的吗?</h1>
        </div>
        <div class="max-w-3xl mx-auto flex flex-col items-center gap-3">
          <a-space wrap>
            <a-button v-for="p in row1" :key="p" class="rounded-2xl h-auto py-2 whitespace-normal text-left" @click="onPrompt(p)">
              {{ p }}
            </a-button>
          </a-space>
          <a-space wrap>
            <a-button v-for="p in row2" :key="p" class="rounded-2xl" @click="onPrompt(p)">{{ p }}</a-button>
          </a-space>
          <a-space wrap>
            <a-button v-for="p in row3" :key="p" class="rounded-2xl" @click="onPrompt(p)">{{ p }}</a-button>
          </a-space>
          <a-space wrap>
            <a-button class="rounded-2xl h-auto py-2 whitespace-normal text-left max-w-lg" @click="onPrompt(row4)">{{ row4 }}</a-button>
          </a-space>
        </div>
      </a-layout-content>

      <a-layout-content v-else class="flex flex-1 min-h-0 overflow-hidden">
        <div class="flex-1 flex flex-col min-w-0 border-r border-gray-200 overflow-hidden">
          <div class="flex-1 overflow-auto p-6 space-y-4">
            <div v-for="(m, i) in messages" :key="i" :class="['max-w-[85%]', m.role === 'user' ? 'ml-auto' : '']">
              <a-card v-if="m.type === 'text'" size="small" :class="m.role === 'user' ? '!bg-[#e6f4ff] border-blue-200' : ''">
                <div v-html="m.html" />
              </a-card>
              <a-card v-else-if="m.type === 'table' && m.rows" size="small">
                <a-table :columns="tableColumns" :data-source="m.rows" :pagination="false" size="small" row-key="orderNo">
                  <template #bodyCell="{ column, record }">
                    <template v-if="column.key === 'orderNo'">
                      <a-typography-link @click="openDetail(record)">{{ record.orderNo }}</a-typography-link>
                    </template>
                    <template v-else-if="column.key === 'progress'">
                      <span class="text-xs text-gray-600">{{ formatProgress(record.currentStepIndex) }}</span>
                    </template>
                  </template>
                </a-table>
              </a-card>
              <a-card v-else-if="m.type === 'followChips'" size="small" class="!border-gray-200 !shadow-sm">
                <div class="flex flex-col gap-2 max-w-lg">
                  <a-button
                    class="!rounded-full !h-auto !py-2.5 !px-4 !flex !justify-between !items-center !text-left !bg-[#f5f5f5] hover:!bg-gray-100 !border-gray-200 !text-gray-800"
                    @click="onFollowChip('returned')"
                  >
                    <span>查询7天内已回单的投诉工单</span>
                    <RightOutlined class="text-gray-400" />
                  </a-button>
                  <a-button
                    class="!rounded-full !h-auto !py-2.5 !px-4 !flex !justify-between !items-center !text-left !bg-[#f5f5f5] hover:!bg-gray-100 !border-gray-200 !text-gray-800"
                    @click="onFollowChip('unreturned')"
                  >
                    <span>查询7天内未回单的投诉工单</span>
                    <RightOutlined class="text-gray-400" />
                  </a-button>
                </div>
              </a-card>
            </div>
          </div>
        </div>
      </a-layout-content>

      <a-drawer
        v-model:open="detailOpen"
        title="投诉处理详情"
        placement="right"
        width="50vw"
        :destroy-on-close="true"
        :body-style="{ background: '#f7f8fa', padding: '16px' }"
      >
        <template v-if="detailRecord">
          <a-space direction="vertical" style="width: 100%" size="middle">
            <!-- 处理进度：放在工单信息上部 -->
            <a-card
              size="small"
              class="!border-gray-200 !shadow-sm"
              :body-style="{ padding: '14px', background: '#fff', border: '1px solid #e5e7eb' }"
            >
              <div class="flex items-center justify-between">
                <div class="text-sm font-semibold text-gray-900">处理进度</div>
                <div class="text-xs text-gray-500">
                  当前环节：<span class="text-gray-900 font-medium">{{ stepLabels[Math.min(Math.max(detailRecord.currentStepIndex, 0), 5)] }}</span>
                </div>
              </div>
              <div class="mt-3 flex flex-wrap gap-2">
                <span
                  v-for="(s, idx) in stepLabels"
                  :key="idx"
                  class="text-xs px-2.5 py-1 rounded-lg"
                  :style="chipStyle(idx, detailRecord.currentStepIndex)"
                >
                  {{ idx + 1 }}. {{ s }}
                </span>
              </div>
            </a-card>

            <a-card
              size="small"
              class="!border-gray-200 !shadow-sm"
              :body-style="{ padding: '14px', background: '#fff', border: '1px solid #e5e7eb' }"
            >
              <div class="text-sm font-semibold text-gray-900">工单信息</div>
              <div class="mt-3 grid grid-cols-2 gap-3 text-xs text-gray-800">
                <div>
                  <div class="text-gray-500">工单编号</div>
                  <div class="font-semibold text-gray-900">{{ detailRecord.orderNo }}</div>
                </div>
                <div>
                  <div class="text-gray-500">投诉号码</div>
                  <div class="text-gray-900">{{ detailRecord.msisdnMasked }}</div>
                </div>
                <div>
                  <div class="text-gray-500">产生时间</div>
                  <div class="text-gray-900">{{ detailRecord.createdAt }}</div>
                </div>
                <div>
                  <div class="text-gray-500">当前环节</div>
                  <div class="text-gray-900">{{ stepLabels[Math.min(Math.max(detailRecord.currentStepIndex, 0), 5)] }}</div>
                </div>
                <div class="col-span-2">
                  <div class="text-gray-500">投诉内容</div>
                  <div class="mt-1 rounded-lg border border-gray-200 bg-gray-50 p-3 text-gray-800">
                    {{ detailRecord.content }}
                  </div>
                </div>
              </div>
            </a-card>

            <a-card
              size="small"
              class="!border-gray-200 !shadow-sm"
              :body-style="{ padding: '14px', background: '#fff', border: '1px solid #e5e7eb' }"
            >
              <div class="text-sm font-semibold text-gray-900">投诉预处理分析结果</div>
              <div class="mt-3 grid grid-cols-2 gap-3 text-xs">
                <div class="rounded-lg border border-gray-200 bg-gray-50 p-3 text-gray-800">
                  <div class="mb-2 text-gray-600">基础签约信息查询结果</div>
                  <div class="flex justify-between"><span class="text-gray-500">用户状态</span><span class="font-medium text-green-700">正常</span></div>
                  <div class="flex justify-between"><span class="text-gray-500">国际漫游权限</span><span class="font-medium text-green-700">已开通</span></div>
                  <div class="flex justify-between"><span class="text-gray-500">数据业务权限</span><span class="font-medium text-green-700">已开通</span></div>
                  <div class="flex justify-between"><span class="text-gray-500">签约 APN</span><span class="text-gray-900">cmnet</span></div>
                  <div class="flex justify-between"><span class="text-gray-500">签约 QoS</span><span class="text-gray-900">QCI=9 · ARP=8</span></div>
                </div>
                <div class="rounded-lg border border-gray-200 bg-gray-50 p-3 text-gray-800">
                  <div class="mb-2 text-gray-600">预处理结论</div>
                  <ul class="list-disc pl-4 space-y-1 text-gray-700">
                    <li>签约侧未发现明显异常，建议进入信令分析定位</li>
                    <li>若复现时间明确，可优先按时间窗拉取关键接口日志</li>
                  </ul>
                </div>
              </div>
            </a-card>

            <a-card
              size="small"
              class="!border-gray-200 !shadow-sm"
              :body-style="{ padding: '14px', background: '#fff', border: '1px solid #e5e7eb' }"
            >
              <div class="text-sm font-semibold text-gray-900">信令分析定位结果</div>
              <div class="mt-2 text-xs text-gray-600">
                当前步骤：<span class="text-gray-900 font-medium">{{ stepLabels[Math.min(Math.max(detailRecord.currentStepIndex, 0), 5)] }}</span>
              </div>
              <div class="mt-3 flex items-center justify-between gap-2">
                <a-space size="small">
                  <a-button size="small" :type="sigTab === 'interaction' ? 'primary' : 'default'" @click="sigTab = 'interaction'">交互消息</a-button>
                  <a-button size="small" :type="sigTab === 'flow' ? 'primary' : 'default'" @click="sigTab = 'flow'">业务流程</a-button>
                </a-space>
                <a-button size="small" @click="onSigUpload"><template #icon><CloudUploadOutlined /></template>信令上传</a-button>
              </div>
              <div class="mt-2 text-[11px] text-gray-500">点击业务流程可在下方查看信令泳道图</div>

              <template v-if="sigTab === 'interaction'">
                <a-table :columns="sigColumns" :data-source="sigRows" :pagination="false" size="small" class="mt-3" row-key="time" />
              </template>
              <template v-else>
                <div class="mt-3 rounded-lg border border-gray-200 bg-gray-50 p-3 text-xs text-gray-800">
                  <div class="mb-2 font-medium text-gray-700">业务流程信令泳道图（示意）</div>
                  <pre class="m-0 overflow-x-auto whitespace-pre text-gray-700">UE | P-CSCF | I-CSCF | S-CSCF | HSS\nREGISTER ->\n<- 403 Forbidden\n</pre>
                </div>
                <div class="mt-3 rounded-lg border border-amber-200 bg-amber-50 p-3 text-xs text-gray-800">
                  <div class="mb-2 font-medium text-amber-900">定位结论</div>
                  <p class="m-0">初步判断为境外漫游网络配置问题，ESM 信息检查失败导致无法完成附着流程。</p>
                </div>
              </template>
            </a-card>

            <a-card
              size="small"
              class="!border-gray-200 !shadow-sm"
              :body-style="{ padding: '14px', background: '#fff', border: '1px solid #e5e7eb' }"
            >
              <div class="text-sm font-semibold text-gray-900">智能体自动回填结论</div>
              <div class="mt-3 rounded-lg border border-gray-200 bg-gray-50 p-3 text-xs text-gray-800">
                初步判断为策略/鉴权链路异常导致用户业务受阻；建议按“策略校验 → 鉴权一致性 → 复现回放”路径处理，并回填工单。
              </div>
              <div class="mt-3 text-xs text-gray-600">建议动作</div>
              <ol class="mt-1 list-decimal space-y-1 pl-4 text-xs text-gray-700">
                <li>核查 PCF 策略下发与用户签约是否匹配（重点：QCI/ARP/漫游策略）</li>
                <li>核查 UDM 鉴权与 SMF/PCF 侧配置一致性，必要时触发重鉴权</li>
                <li>如已恢复，补充闭环确认与复发监控</li>
              </ol>
              <div class="mt-3 text-[11px] text-gray-500">回填时间：2024-05-13 08:15:32（示例）</div>
            </a-card>

            <p class="text-xs text-gray-500">本侧栏不包含原投诉详情页中的「投诉智能体」对话区域；数据由后端接口返回，前端仅动态渲染。</p>
          </a-space>
        </template>
      </a-drawer>

      <div class="border-t border-gray-200 bg-white px-4 py-3 shrink-0">
        <div class="max-w-4xl mx-auto">
          <div class="flex flex-wrap items-center gap-2 mb-2">
            <a-upload :show-upload-list="false">
              <a-button size="small">
                <template #icon><PaperClipOutlined /></template>
                附件
              </a-button>
            </a-upload>
            <a-radio-group v-model:value="mode" size="small" button-style="solid">
              <a-radio-button value="think">思考模式</a-radio-button>
              <a-radio-button value="normal">普通模式</a-radio-button>
            </a-radio-group>
            <a-divider type="vertical" class="!mx-1" />
            <span class="text-xs text-gray-500">子智能体</span>
            <a-radio-group v-model:value="agent" size="small">
              <a-radio-button value="fault">故障抢通</a-radio-button>
              <a-radio-button value="alarm">告警处理</a-radio-button>
              <a-radio-button value="complaint">投诉处理</a-radio-button>
              <a-radio-button value="script">脚本核查</a-radio-button>
            </a-radio-group>
          </div>
          <a-input-search v-model:value="input" placeholder="发消息…" size="large" enter-button @search="send" />
        </div>
      </div>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { PaperClipOutlined, CloudUploadOutlined, RightOutlined } from '@ant-design/icons-vue';
import { fetchComplaintOrders, type ComplaintOrderRow } from '@/api/complaint/order';

const history = ['查询北京今日告警工单', '全省语音业务指标巡检'];
const row1 = ['请查询最近1天全国核心网运行情况；'];
const row2 = ['请查询青海最近7天的告警工单；', '请查询青海最近7天的投诉工单；'];
const row3 = ['请查询西藏最近7天的告警工单；', '请查询西藏最近7天的投诉工单；'];
const row4 = '如何针对割接脚本进行自动核查？';

const stepLabels = ['自动接单', '分类提参', '签约查询', '信令分析', '工单回填', '闭环确认'];

const view = ref<'home' | 'session'>('home');
const headerLabel = computed(() => (view.value === 'home' ? '新对话' : '对话'));
type ChatMsg =
  | { role: 'user' | 'ai'; type: 'text'; html: string }
  | { role: 'ai'; type: 'table'; rows: ComplaintOrderRow[] }
  | { role: 'ai'; type: 'followChips' };

const messages = ref<ChatMsg[]>([]);
const input = ref('');
const mode = ref<'think' | 'normal'>('normal');
const agent = ref('complaint');

const tableColumns = [
  { title: '编号', dataIndex: 'id', key: 'id', width: 64 },
  { title: '工单编号', key: 'orderNo', width: 168 },
  { title: '投诉号码', dataIndex: 'msisdnMasked', key: 'msisdn' },
  { title: '投诉内容', dataIndex: 'content', key: 'content', ellipsis: true },
  { title: '产生时间', dataIndex: 'createdAt', key: 'createdAt', width: 160 },
  { title: '工单处理进度', key: 'progress', width: 220 },
];

const detailOpen = ref(false);
const detailRecord = ref<ComplaintOrderRow | null>(null);
const sigTab = ref<'interaction' | 'flow'>('interaction');

const sigColumns = [
  { title: '时间', dataIndex: 'time', key: 'time', width: 180 },
  { title: '主叫', dataIndex: 'caller', key: 'caller', width: 140 },
  { title: '被叫', dataIndex: 'callee', key: 'callee', width: 110 },
  { title: '网元节点', dataIndex: 'node', key: 'node', width: 140 },
  { title: '消息', dataIndex: 'msg', key: 'msg', width: 120 },
  { title: '结果', dataIndex: 'result', key: 'result', width: 90 },
  { title: '时延(s)', dataIndex: 'delay', key: 'delay', width: 90 },
] as const;

const sigRows = [
  { time: '2025-12-01 15:22:44.170', caller: '+8613******22', callee: '05711****', node: 'UE→P-CSCF', msg: 'INVITE', result: '成功', delay: '2.802' },
  { time: '2025-12-01 15:22:44.210', caller: '+8613******22', callee: '05711****', node: 'P-CSCF→I-CSCF', msg: 'INVITE', result: '成功', delay: '0.120' },
  { time: '2025-12-01 15:22:44.520', caller: '+8613******22', callee: '05711****', node: 'S-CSCF→P-CSCF', msg: '100 TRYING', result: '成功', delay: '0.090' },
  { time: '2025-12-01 15:22:47.020', caller: '+8613******22', callee: '05711****', node: 'P-CSCF→UE', msg: 'CANCEL', result: '失败', delay: '0.060' },
];

function formatProgress(idx: number) {
  const i = Math.min(Math.max(idx, 0), 5);
  return `当前环节：${stepLabels[i]}（${stepLabels.join(' → ')}）`;
}

function resetHome() {
  view.value = 'home';
  messages.value = [];
  detailOpen.value = false;
}

function openDetail(r: ComplaintOrderRow) {
  detailRecord.value = r;
  detailOpen.value = true;
  sigTab.value = 'interaction';
}

function chipStyle(idx: number, current: number) {
  const c = Math.min(Math.max(current, 0), 5);
  if (idx < c) return { background: 'rgba(16,185,129,.12)', border: '1px solid rgba(16,185,129,.35)', color: '#047857' };
  if (idx === c) return { background: 'rgba(59,130,246,.1)', border: '1px solid rgba(59,130,246,.35)', color: '#1d4ed8' };
  return { background: '#f5f5f5', border: '1px solid #e5e7eb', color: '#6b7280' };
}

function onFollowChip(kind: 'returned' | 'unreturned') {
  const text = kind === 'returned' ? '查询7天内已回单的投诉工单' : '查询7天内未回单的投诉工单';
  messages.value.push({ role: 'user', type: 'text', html: escapeHtml(text) });
  messages.value.push({
    role: 'ai',
    type: 'text',
    html: '<p class="text-gray-700">（演示）该问题已记录，实际应答由后端接口返回。</p>',
  });
}

function onSigUpload() {
  // 演示交互：真实上传应对接后端上传接口，异步解析生成交互消息/业务流程/泳道图
  window.alert('已提交信令上传任务，正在解析生成交互消息/业务流程/泳道图…（演示）');
}
function isQinghaiComplaint(text: string) {
  return /青海/.test(text) && /投诉/.test(text) && (/7|七/.test(text) || /最近/.test(text));
}

function escapeHtml(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

async function onPrompt(text: string) {
  input.value = text;
  await send();
}

async function send() {
  const text = input.value.trim();
  if (!text) return;
  view.value = 'session';
  messages.value.push({ role: 'user', type: 'text', html: escapeHtml(text) });
  input.value = '';

  if (isQinghaiComplaint(text)) {
    let rows: ComplaintOrderRow[] = [];
    try {
      const res = await fetchComplaintOrders('QH', 7);
      rows = res.data?.records ?? [];
    } catch {
      rows = mockRows();
    }
    messages.value.push({
      role: 'ai',
      type: 'text',
      html: `<p>已为您查询<strong>青海省最近7天</strong>的投诉工单，共 <strong>${rows.length}</strong> 条，见下表，您可以点击工单编号来查看投诉处理详情内容。</p>`,
    });
    messages.value.push({ role: 'ai', type: 'table', rows });
    messages.value.push({ role: 'ai', type: 'followChips' });
    return;
  }

  messages.value.push({
    role: 'ai',
    type: 'text',
    html: '<p>（演示）该问题已记录，实际应答由后端智能体接口返回。</p>',
  });
}

function mockRows(): ComplaintOrderRow[] {
  return [
    { id: 1, orderNo: 'QH-063-250401-00001', msisdnMasked: '139****9733', content: '漫游地数据无法激活', createdAt: '2025-04-08 09:12:33', currentStepIndex: 3 },
    { id: 2, orderNo: 'QH-063-250407-00015', msisdnMasked: '136****8818', content: '语音主叫单通', createdAt: '2025-04-07 14:22:01', currentStepIndex: 5 },
    { id: 3, orderNo: 'QH-063-250405-00008', msisdnMasked: '155****1200', content: '物联网卡速率不达标', createdAt: '2025-04-05 11:05:44', currentStepIndex: 2 },
  ];
}


</script>
