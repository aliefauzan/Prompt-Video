// Person instance masks (Apple Vision VNGeneratePersonInstanceMaskRequest) for every PNG in a dir.
// Writes <out_dir>/frame_NNN.png: 8-bit label image at full frame size, 0 = background,
// 1..n = person instance (labels are per frame, not tracked).
// usage: swift instances.swift <in_dir> <out_dir>   (or swiftc -O instances.swift -o instances: ~50x faster)
import Foundation
import Vision
import ImageIO
import CoreImage
import UniformTypeIdentifiers

let args = CommandLine.arguments
let inDir = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2])
try FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
let files = try FileManager.default.contentsOfDirectory(atPath: inDir.path)
    .filter { $0.hasSuffix(".png") }.sorted()

for name in files {
    let url = inDir.appendingPathComponent(name)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else { continue }
    let req = VNGeneratePersonInstanceMaskRequest()
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try handler.perform([req])
    let W = cg.width, H = cg.height
    var label = [UInt8](repeating: 0, count: W * H)
    var best = [Float](repeating: 0.5, count: W * H)
    if let obs = req.results?.first {
        for inst in obs.allInstances {
            let pb = try obs.generateScaledMaskForImage(forInstances: IndexSet(integer: inst), from: handler)
            CVPixelBufferLockBaseAddress(pb, .readOnly)
            let bw = CVPixelBufferGetWidth(pb), bh = CVPixelBufferGetHeight(pb)
            let rb = CVPixelBufferGetBytesPerRow(pb)
            let base = CVPixelBufferGetBaseAddress(pb)!
            for y in 0..<min(bh, H) {
                let row = base.advanced(by: y * rb).assumingMemoryBound(to: Float32.self)
                for x in 0..<min(bw, W) {
                    let v = row[x]
                    if v > best[y * W + x] { best[y * W + x] = v; label[y * W + x] = UInt8(inst) }
                }
            }
            CVPixelBufferUnlockBaseAddress(pb, .readOnly)
        }
    }
    let cs = CGColorSpaceCreateDeviceGray()
    let ctx = CGContext(data: &label, width: W, height: H, bitsPerComponent: 8, bytesPerRow: W,
                        space: cs, bitmapInfo: CGImageAlphaInfo.none.rawValue)!
    let img = ctx.makeImage()!
    let dst = CGImageDestinationCreateWithURL(outDir.appendingPathComponent(name) as CFURL,
                                              UTType.png.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dst, img, nil)
    CGImageDestinationFinalize(dst)
}
print("frames:", files.count)
