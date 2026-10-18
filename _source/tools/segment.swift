// Person segmentation for every PNG in an input dir, written as grayscale PNG masks.
// usage: swift segment.swift <in_dir> <out_dir>
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let inDir = URL(fileURLWithPath: args[1])
let outDir = URL(fileURLWithPath: args[2])
try? FileManager.default.createDirectory(at: outDir, withIntermediateDirectories: true)
let ctx = CIContext()
let files = try FileManager.default.contentsOfDirectory(atPath: inDir.path)
    .filter { $0.hasSuffix(".png") }.sorted()

for name in files {
    let url = inDir.appendingPathComponent(name)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let cg = CGImageSourceCreateImageAtIndex(src, 0, nil) else { continue }
    let req = VNGeneratePersonSegmentationRequest()
    req.qualityLevel = .accurate
    req.outputPixelFormat = kCVPixelFormatType_OneComponent8
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    try handler.perform([req])
    guard let buf = req.results?.first?.pixelBuffer else { continue }
    var mask = CIImage(cvPixelBuffer: buf)
    let sx = CGFloat(cg.width) / mask.extent.width
    let sy = CGFloat(cg.height) / mask.extent.height
    mask = mask.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
    let out = outDir.appendingPathComponent(name)
    guard let outCG = ctx.createCGImage(mask, from: CGRect(x: 0, y: 0, width: cg.width, height: cg.height),
                                         format: .L8, colorSpace: CGColorSpaceCreateDeviceGray()),
          let dest = CGImageDestinationCreateWithURL(out as CFURL, UTType.png.identifier as CFString, 1, nil)
    else { continue }
    CGImageDestinationAddImage(dest, outCG, nil)
    CGImageDestinationFinalize(dest)
    print(name)
}
