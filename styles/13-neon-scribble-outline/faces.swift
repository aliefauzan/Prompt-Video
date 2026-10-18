// Face boxes + landmarks (Apple Vision) for every PNG in a dir, written as one JSON.
// Points are in image pixels, origin top-left.
// usage: swift faces.swift <in_dir> <out.json>
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
    let req = VNDetectFaceLandmarksRequest()
    try VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    var faces: [[String: Any]] = []
    for f in req.results ?? [] {
        let b = f.boundingBox
        var face: [String: Any] = ["box": [b.minX * W, (1 - b.maxY) * H, b.width * W, b.height * H]]
        if let lm = f.landmarks {
            let parts: [(String, VNFaceLandmarkRegion2D?)] = [
                ("leftEye", lm.leftEye), ("rightEye", lm.rightEye),
                ("leftEyebrow", lm.leftEyebrow), ("rightEyebrow", lm.rightEyebrow),
                ("outerLips", lm.outerLips), ("innerLips", lm.innerLips),
                ("nose", lm.nose), ("faceContour", lm.faceContour),
                ("leftPupil", lm.leftPupil), ("rightPupil", lm.rightPupil),
            ]
            for (k, r) in parts {
                guard let r = r else { continue }
                face[k] = r.pointsInImage(imageSize: CGSize(width: W, height: H)).map { [$0.x, H - $0.y] }
            }
        }
        faces.append(face)
    }
    all[name] = faces
}
let data = try JSONSerialization.data(withJSONObject: all, options: [.sortedKeys])
try data.write(to: URL(fileURLWithPath: args[2]))
print("faces:", all.count)
