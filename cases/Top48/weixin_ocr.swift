// macOS 上的可选本地截图文字定位；不上传图片，不需要第三方 OCR 服务。
import Foundation
import Vision

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.recognitionLanguages = ["zh-Hans", "en-US"]
request.customWords = ["测试", "测试账号", "微信", "朋友圈", "发送", "预览", "拍摄"]
request.usesLanguageCorrection = false
try VNImageRequestHandler(url: URL(fileURLWithPath: CommandLine.arguments[1])).perform([request])
var rows = (request.results ?? []).compactMap { item -> [String: Any]? in
    guard let candidate = item.topCandidates(1).first else { return nil }
    let box = item.boundingBox
    return ["text": candidate.string, "x": box.minX, "y": 1-box.maxY,
            "w": box.width, "h": box.height, "confidence": candidate.confidence]
}
let json = try JSONSerialization.data(withJSONObject: rows)
print(String(data: json, encoding: .utf8)!)
