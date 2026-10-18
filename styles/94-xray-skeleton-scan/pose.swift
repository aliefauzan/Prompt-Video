// Body + hand joints (Apple Vision) for every PNG in a dir, written as one JSON.
// Points are in image pixels, origin top-left:
// {"frame_001.png": {"bodies": [{joint: [x, y, conf]}], "hands": [...], "faces": [{"box": [x, y, w, h], "leftPupil": [x, y], ...}]}}
// usage: swift pose.swift <in_dir> <out.json>
import Foundation
import Vision
import ImageIO

let args = CommandLine.arguments
let inDir = URL(fileURLWithPath: args[1])
let files = try FileManager.default.contentsOfDirectory(atPath: inDir.path)
    .filter { $0.hasSuffix(".png") }.sorted()
var all: [String: Any] = [:]

for name in files {
    let url = inDir.appendingPathComponent(name)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else { continue }
    let W = CGFloat(cg.width), H = CGFloat(cg.height)
    let body = VNDetectHumanBodyPoseRequest()
    let hand = VNDetectHumanHandPoseRequest()
    hand.maximumHandCount = 6
    let face = VNDetectFaceLandmarksRequest()
    try VNImageRequestHandler(cgImage: cg, options: [:]).perform([body, hand, face])
    var bodies: [[String: Any]] = []
    for o in body.results ?? [] {
        var j: [String: Any] = [:]
        for (k, p) in try o.recognizedPoints(.all) where p.confidence > 0.1 {
            j[k.rawValue.rawValue] = [p.location.x * W, (1 - p.location.y) * H, Double(p.confidence)]
        }
        bodies.append(j)
    }
    var hands: [[String: Any]] = []
    for o in hand.results ?? [] {
        var j: [String: Any] = [:]
        for (k, p) in try o.recognizedPoints(.all) where p.confidence > 0.1 {
            j[k.rawValue.rawValue] = [p.location.x * W, (1 - p.location.y) * H, Double(p.confidence)]
        }
        hands.append(j)
    }
    var faces: [[String: Any]] = []
    for f in face.results ?? [] {
        let b = f.boundingBox
        var o: [String: Any] = ["box": [b.minX * W, (1 - b.maxY) * H, b.width * W, b.height * H],
                                "roll": f.roll?.doubleValue ?? 0]
        if let lm = f.landmarks {
            for (k, r) in [("leftPupil", lm.leftPupil), ("rightPupil", lm.rightPupil)] {
                if let p = r?.pointsInImage(imageSize: CGSize(width: W, height: H)).first {
                    o[k] = [p.x, H - p.y]
                }
            }
        }
        faces.append(o)
    }
    all[name] = ["bodies": bodies, "hands": hands, "faces": faces]
}
let data = try JSONSerialization.data(withJSONObject: all, options: [.sortedKeys])
try data.write(to: URL(fileURLWithPath: args[2]))
print("frames:", all.count)
