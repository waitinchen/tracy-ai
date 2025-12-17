# Partial Book 模式技術規範

**文件性質**: **明確技術指揮令**（必須遵守）  
**適用範圍**: 電子書童專案  
**資料來源**: `C:\Users\waiti\tracy-ai\換框` 資料夾  
**最後更新**: 2025-01-XX

---

## ⚠️ 重要聲明

**這不是建議，是必須遵守的行為規範與技術落點。**

Partial Book 模式是「合法狀態」，不是過渡 Bug。

---

## 一、模式定義（不可誤解）

### 1.1 系統層標記

系統層必須明確標記：

```typescript
bookStatus = 'PARTIAL'
```

此狀態需影響：

* ✅ 查詢行為
* ✅ 回應措辭
* ✅ 引用策略
* ✅ 驗證規則

❗ **禁止任何假裝「全書已齊」的行為。**

---

## 二、資料層指揮

### 2.1 Canonical Text Store（未完成版）

請將 `換框` 資料夾內**每一個檔案**視為一個 Fragment。

#### Fragment 規範

```typescript
interface Fragment {
  fragmentId: string;      // 穩定 ID，例如 F01, F02
  sourceType: 'docx' | 'pdf' | 'png' | 'xlsx';
  title: string;           // 來自檔名
  content: string | Blob;  // 原文 / OCR / 表格
  status: 'confirmed';     // 只能是 confirmed，不得推論缺失
  sourcePath: string;      // 原始檔案路徑
}
```

#### 當前 Fragment 列表（來自 `換框` 資料夾）

| Fragment ID | 檔名 | 類型 | 狀態 |
|------------|------|------|------|
| F01 | `什麼是換框.docx` | docx | confirmed |
| F02 | `情緒詞表.xlsx` | xlsx | confirmed |
| F03 | `換框八法_舉例.pdf` | pdf | confirmed |
| F04 | `換框八法_說明.docx` | docx | confirmed |
| F05 | `換框八法_金句.docx` | docx | confirmed |
| F06 | `換框思維力_序.docx` | docx | confirmed |
| F07 | `換框思維力.png` | png | confirmed |
| F08 | `換框案例參考.xlsx` | xlsx | confirmed |
| F09 | `視覺換框舉例.png` | png | confirmed |
| F10 | `角色換框舉例.png` | png | confirmed |

#### ⚠️ 禁止事項

* ❌ 合併 Fragment
* ❌ 重排順序
* ❌ 補寫不存在的章節
* ❌ 推論缺失內容
* ❌ 假裝完整性

---

### 2.2 Provisional Structure（臨時結構層）

允許存在「暫時群組」，但**不可稱為章節**。

```typescript
interface Cluster {
  id: string;              // 例如 C1, C2
  label: string;           // 例如「核心概念」「操作方法」
  fragments: string[];    // Fragment ID 陣列，例如 [F01]
}
```

#### 臨時群組範例

```yaml
clusters:
  - id: C1
    label: 核心概念
    fragments: [F01, F06]

  - id: C2
    label: 換框八法
    fragments: [F03, F04, F05]

  - id: C3
    label: 案例與舉例
    fragments: [F08, F09, F10]

  - id: C4
    label: 輔助工具
    fragments: [F02]
```

#### 這一層的原則

* ✅ 只做定位
* ✅ 不做敘事
* ✅ 不做完整性假設
* ❌ 不可稱為「章節」
* ❌ 不可暗示順序或完整性

---

## 三、行為層規範（最重要）

### 3.1 電子書童「必須知道資料不完整」

在 API 層引入：

```typescript
context.bookCompleteness = 'PARTIAL';
```

#### 影響行為

**禁止**:
* ❌ 不可說「後面會提到」
* ❌ 不可說「書中接下來會說」
* ❌ 不可補齊作者邏輯
* ❌ 不可說「在下一章會說明」
* ❌ 不可整體觀點整理
* ❌ 不可方法論補齊
* ❌ 不可架構性總結

**允許**:
* ✅ 可以說「目前素材只到這裡」
* ✅ 可以引導回到 Fragment 原文
* ✅ 可以說「在這段素材裡」
* ✅ 可以承認「資料不完整」

---

### 3.2 引用策略（Partial 專屬）

BookService 在 PARTIAL 模式下，必須再加一層限制：

```typescript
if (bookStatus === 'PARTIAL') {
  maxQuotes = 1;  // 不是 2，是 1
}
```

#### 原則

> Partial 模式下，**寧可只給一段，也不給兩段**。

#### 實作要求

```typescript
// Partial 模式：最多 1 段
const MAX_QUOTES_PARTIAL = 1;

// Complete 模式：最多 1-2 段
const MAX_QUOTES_COMPLETE = 2;
```

#### 禁止跨 Fragment 拼接

```typescript
// ❌ 錯誤：跨 Fragment 拼接
const quote1 = fragment1.content;
const quote2 = fragment2.content;
return `${quote1}...${quote2}`;  // 禁止

// ✅ 正確：只返回單一 Fragment 的內容
const quote = fragment.content;
return quote;  // 只返回一個 Fragment
```

---

### 3.3 三步驟回應流程（不變，但更克制）

三步驟仍然存在，但語氣需符合 Partial 模式：

#### Step 1｜溫柔承接

**Partial 模式**:
- 只承認讀者停在哪個片段
- 「我聽見你在想這個。你現在停在這段素材裡。」

**Complete 模式**:
- 「我聽見你在想這件事。」

#### Step 2｜溫和轉向

**Partial 模式**:
- 轉向 Fragment，而非概念
- 「在這段素材裡，作者寫的是：...」
- 「目前素材只到這裡。我們可以回到這個片段，再慢慢讀一次。」

**Complete 模式**:
- 「在這一章裡，作者寫的是：...」

#### Step 3｜留白邀請

**Partial 模式**:
- 明確停住，不延展
- 「如果是你，你現在怎麼讀這段素材？」

**Complete 模式**:
- 「如果是你，你現在怎麼讀這一段？」

---

## 四、向量化的明確指令

### 4.1 可以做（選配）

* ✅ 僅對 Fragment 做 embedding
* ✅ 僅回傳 fragmentId 作為候選
* ✅ 使用向量作為「路標」

### 4.2 絕對禁止

* ❌ 用向量結果直接生成回應
* ❌ 用向量跨 Fragment 拼接內容
* ❌ 用向量補齊書的邏輯
* ❌ 用向量推論缺失內容

> **向量 = 路標，不是地圖**

---

## 五、測試與驗收（必須通過）

### 5.1 測試情境

以下情境必須通過：

#### 情境 1: 使用者問「這本書後面怎麼說？」

**預期回應**:
- ❌ 不得回答內容
- ✅ 必須說「目前素材只到這裡」
- ✅ 可以引導回到現有 Fragment

**範例**:
> 「目前素材只到這裡。我們可以回到這段素材，再慢慢讀一次。」

#### 情境 2: 使用者要求「幫我總結整本書」

**預期回應**:
- ❌ 必須拒絕或沉默
- ✅ 可以說「目前素材不完整，無法總結整本書」

**範例**:
> 「我聽見你在想這個。目前素材不完整，我無法總結整本書。我們可以回到這段素材，再慢慢讀一次。」

#### 情境 3: 使用者跨 Fragment 問概念

**預期回應**:
- ❌ 只能指回單一 Fragment
- ✅ 不能跨 Fragment 拼接內容
- ✅ 不能補齊邏輯

**範例**:
> 「我聽見你在想這個。這個概念出現在這段素材裡：[引用單一 Fragment]。目前素材只到這裡。」

---

### 5.2 驗收標準

Partial Book 模式的成功標準不是「撐住功能」，而是：

> **系統在資料不完整時，依然不會多說一句。**

這不是降級，是文明設計。

---

## 六、技術實作要點

### 6.1 BookService 改造

```typescript
// app/lib/books/book-service.ts

export class BookService {
  private bookStatus: 'COMPLETE' | 'PARTIAL';
  
  constructor(contentPath: string) {
    // 載入 Fragment
    const fragments = this.loadFragmentsFromDirectory(contentPath);
    
    // 明確標記狀態
    this.bookStatus = fragments.length > 0 ? 'PARTIAL' : 'COMPLETE';
    
    console.log(`[BookService] Book Status: ${this.bookStatus}`);
  }
  
  getBookStatus(): 'COMPLETE' | 'PARTIAL' {
    return this.bookStatus;
  }
  
  async findRelevantQuotes(
    question: string,
    currentFragmentId?: string
  ): Promise<Quote[]> {
    if (this.bookStatus === 'PARTIAL') {
      // Partial 模式：最多 1 段
      return this.findRelevantQuotesPartial(question, currentFragmentId);
    } else {
      // Complete 模式：最多 1-2 段
      return this.findRelevantQuotesComplete(question);
    }
  }
  
  private async findRelevantQuotesPartial(
    question: string,
    currentFragmentId?: string
  ): Promise<Quote[]> {
    // 只在現有 Fragment 中搜索
    // 不跨 Fragment 拼接
    // 最多返回 1 段
    const maxQuotes = 1;  // 硬限制
    
    // ... 實作邏輯
  }
}
```

### 6.2 Chat API Context 改造

```typescript
// app/api/chat/route.ts

export async function POST(request: Request) {
  // ...
  
  // 獲取書籍狀態
  const bookStatus = bookService.getBookStatus();
  const bookCompleteness = bookStatus === 'PARTIAL' ? 'PARTIAL' : 'COMPLETE';
  
  // 傳入 context
  const context = {
    bookCompleteness,
    currentFragmentId,
    // ...
  };
  
  // 生成回應時使用 context
  const response = await generateResponse(messages, context);
  
  // ...
}
```

### 6.3 ResponseGenerator 改造

```typescript
// app/lib/response/response-generator.ts

export class ResponseGenerator {
  async generate(
    input: string,
    context: {
      bookCompleteness: 'PARTIAL' | 'COMPLETE';
      quotes: Quote[];
      currentFragmentId?: string;
    }
  ): Promise<string> {
    if (context.bookCompleteness === 'PARTIAL') {
      // Partial 模式：更克制的回應
      return this.generatePartialResponse(input, context);
    } else {
      // Complete 模式：一般回應
      return this.generateCompleteResponse(input, context);
    }
  }
  
  private generatePartialResponse(
    input: string,
    context: any
  ): string {
    // Partial 模式專屬邏輯
    // 禁止：整體觀點整理、方法論補齊、架構性總結
  }
}
```

---

## 七、最難守住的地方（工程直覺想越線的地方）

### 7.1 向量搜索的誘惑

**工程直覺**: 用向量搜索跨 Fragment 找相關內容，然後拼接

**必須守住**: 
- 向量只能作為「路標」，不能直接生成回應
- 不能跨 Fragment 拼接
- 不能補齊邏輯

**實作策略**:
```typescript
// ✅ 正確：向量只返回 fragmentId
const candidateFragments = await vectorSearch(question);
// 返回: [F01, F03]  // 只返回 ID

// 然後只從單一 Fragment 提取內容
const quote = await extractFromFragment(candidateFragments[0]);
// 只返回一個 Fragment 的內容

// ❌ 錯誤：向量直接生成回應
const response = await vectorSearchAndGenerate(question);
// 禁止：可能跨 Fragment 拼接
```

---

### 7.2 LLM 的「補齊本能」

**工程直覺**: LLM 會自動補齊邏輯，讓回應更完整

**必須守住**:
- 禁止 LLM 補齊作者邏輯
- 禁止推論缺失內容
- 必須明確標記「資料不完整」

**實作策略**:
```typescript
// 在 System Prompt 中明確標記
const systemPrompt = `
# 【Partial Book 模式】

目前書籍資料不完整，只有部分 Fragment。

禁止：
- 補齊作者邏輯
- 推論缺失內容
- 說「後面會提到」
- 整體觀點整理

必須：
- 明確說「目前素材只到這裡」
- 只引用現有 Fragment
- 不跨 Fragment 拼接
`;
```

---

### 7.3 引用數量的誘惑

**工程直覺**: 給更多引用，讓回應更豐富

**必須守住**:
- Partial 模式：最多 1 段（不是 2 段）
- 寧可少給，也不多給

**實作策略**:
```typescript
// 硬限制常數
const MAX_QUOTES_PARTIAL = 1;  // 不是 2

// 嚴格執行
const quotes = candidateQuotes.slice(0, MAX_QUOTES_PARTIAL);
// 即使找到很多相關內容，也只返回 1 段
```

---

### 7.4 三步驟流程的「完整性誘惑」

**工程直覺**: 三步驟回應應該更完整、更有幫助

**必須守住**:
- Partial 模式下更克制
- 不延展概念
- 不補齊邏輯

**實作策略**:
```typescript
// Partial 模式專屬的 Step 2
if (bookStatus === 'PARTIAL') {
  // 只轉向 Fragment，不延展概念
  return `在這段素材裡，作者寫的是：${quote.text}\n\n目前素材只到這裡。`;
} else {
  // Complete 模式：一般轉向
  return `在這一章裡，作者寫的是：${quote.text}`;
}
```

---

## 八、實作檢查清單

### 8.1 資料層

- [ ] Fragment 系統已實作
- [ ] 每個檔案成為一個 Fragment
- [ ] 禁止合併、重排、補寫
- [ ] Provisional Structure 已建立（可選）

### 8.2 行為層

- [ ] `bookStatus = 'PARTIAL'` 已標記
- [ ] `context.bookCompleteness` 已傳入
- [ ] 引用策略：Partial 模式最多 1 段
- [ ] 三步驟流程：Partial 模式更克制
- [ ] 禁止說「後面會提到」
- [ ] 禁止補齊作者邏輯

### 8.3 驗證層

- [ ] 驗證器檢查是否假裝全書已齊
- [ ] 驗證器檢查是否跨 Fragment 拼接
- [ ] 驗證器檢查是否補齊邏輯

### 8.4 測試

- [ ] 測試情境 1 通過
- [ ] 測試情境 2 通過
- [ ] 測試情境 3 通過

---

## 九、總結

### 9.1 核心原則

> **系統在資料不完整時，依然不會多說一句。**

### 9.2 成功標準

Partial Book 模式的成功標準不是「撐住功能」，而是：

* ✅ 系統明確知道資料不完整
* ✅ 系統不會假裝全書已齊
* ✅ 系統不會補齊邏輯
* ✅ 系統不會跨 Fragment 拼接
* ✅ 系統在資料不完整時，依然不會多說一句

這不是降級，是文明設計。

---

**文件版本**: v1.0  
**最後更新**: 2025-01-XX  
**維護者**: 開發團隊

