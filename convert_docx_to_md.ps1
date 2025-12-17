# 转换 DOCX 到 Markdown
$docxPath = "temp_docx\word\document.xml"
$outputPath = "Tracy_converted.md"

# 读取 XML 文件
[xml]$xml = Get-Content $docxPath -Encoding UTF8

# 定义命名空间
$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace("w", "http://schemas.openxmlformats.org/wordprocessingml/2006/main")

# 提取所有段落文本
$paragraphs = $xml.SelectNodes("//w:p", $ns)
$markdown = @()

foreach ($para in $paragraphs) {
    $text = ""
    $runs = $para.SelectNodes(".//w:t", $ns)
    
    foreach ($run in $runs) {
        $text += $run.InnerText
    }
    
    if ($text.Trim() -ne "") {
        # 检查是否是标题（通过样式或其他方式判断）
        $pPr = $para.SelectSingleNode(".//w:pPr", $ns)
        if ($pPr) {
            $pStyle = $pPr.SelectSingleNode(".//w:pStyle", $ns)
            if ($pStyle) {
                $style = $pStyle.GetAttribute("w:val")
                if ($style -like "*Heading*" -or $style -like "*Title*") {
                    $level = 1
                    if ($style -match "Heading(\d+)") {
                        $level = [int]$matches[1]
                    }
                    $markdown += "#" * $level + " " + $text.Trim()
                    continue
                }
            }
        }
        
        # 检查文本是否看起来像标题（全大写、短文本等）
        if ($text.Trim().Length -lt 50 -and $text.Trim() -cmatch "^[A-Z\s]+$") {
            $markdown += "## " + $text.Trim()
        } else {
            $markdown += $text.Trim()
        }
    }
}

# 写入 Markdown 文件
$markdown -join "`n`n" | Out-File -FilePath $outputPath -Encoding UTF8

Write-Host "转换完成！输出文件: $outputPath"

