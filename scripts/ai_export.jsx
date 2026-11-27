// Batch-export logo SVGs with Adobe Illustrator:
//   <ROOT>/SVG/*.svg  →  <ROOT>/RGB/{AI,PDF}  and  <ROOT>/CMYK/{AI,EPS,PDF}
// CMYK uses the brand-specified values from <ROOT>/cmyk.json (not ICC auto-conversion), e.g.
//   { "2F6BFF": [85,55,0,0], "111827": [0,0,0,100], "FFFFFF": [0,0,0,0], "000000": [0,0,0,100] }
//
// Run (macOS):
//   sed "s|__ROOT__|/abs/path/to/logo|" ai_export.jsx > /tmp/run.jsx
//   osascript -e 'with timeout of 900 seconds' \
//     -e 'tell application id "com.adobe.illustrator" to do javascript file (POSIX file "/tmp/run.jsx")' \
//     -e 'end timeout'
// (Beta: application id "com.adobe.illustratorBeta")
#target illustrator
(function () {
  var ROOT = "__ROOT__";
  var cfg = new File(ROOT + "/cmyk.json"); cfg.open("r"); var MAP = eval("(" + cfg.read() + ")"); cfg.close();
  var dirs = ["/RGB/AI", "/RGB/PDF", "/CMYK/AI", "/CMYK/EPS", "/CMYK/PDF"];
  for (var d = 0; d < dirs.length; d++) new Folder(ROOT + dirs[d]).create();

  function hex(c) {
    function h(v) { var s = Math.round(v).toString(16).toUpperCase(); return s.length < 2 ? "0" + s : s; }
    return h(c.red) + h(c.green) + h(c.blue);
  }
  function cmyk(a) { var c = new CMYKColor(); c.cyan = a[0]; c.magenta = a[1]; c.yellow = a[2]; c.black = a[3]; return c; }

  app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;   // a dialog would hang the batch
  var files = new Folder(ROOT + "/SVG").getFiles("*.svg"), log = [], miss = [];
  for (var i = 0; i < files.length; i++) {
    var base = decodeURI(files[i].name).replace(/\.svg$/i, "");
    var doc = app.open(files[i]);
    doc.artboards[0].artboardRect = doc.visibleBounds;

    var ai = new IllustratorSaveOptions(); ai.compatibility = Compatibility.ILLUSTRATOR17; ai.pdfCompatible = true;
    var pdf = new PDFSaveOptions(); pdf.compatibility = PDFCompatibility.ACROBAT7; pdf.preserveEditability = true;
    doc.saveAs(new File(ROOT + "/RGB/AI/" + base + ".ai"), ai);
    doc.saveAs(new File(ROOT + "/RGB/PDF/" + base + ".pdf"), pdf);

    // CMYK: record each path's RGB, then copy the art into a NEW CMYK document. The menu command
    // "doc-color-cmyk" silently does nothing on some builds (seen on Illustrator 31 beta), which leaves
    // an RGB document and lets the PDF preset invent its own separations.
    var cols = [];
    for (var p = 0; p < doc.pathItems.length; p++) {
      var it = doc.pathItems[p];
      cols.push(it.filled && it.fillColor.typename == "RGBColor" ? hex(it.fillColor) : null);
    }
    var ab = doc.artboards[0].artboardRect;
    var cdoc = app.documents.add(DocumentColorSpace.CMYK, ab[2] - ab[0], ab[1] - ab[3]);
    if (cdoc.documentColorSpace != DocumentColorSpace.CMYK) throw new Error("could not create a CMYK document");
    cdoc.artboards[0].artboardRect = ab;
    for (var g = doc.pageItems.length - 1; g >= 0; g--) {
      if (doc.pageItems[g].parent.typename == "Layer")
        doc.pageItems[g].duplicate(cdoc.layers[0], ElementPlacement.PLACEATBEGINNING);
    }
    doc.close(SaveOptions.DONOTSAVECHANGES);
    doc = cdoc;
    if (doc.pathItems.length != cols.length) throw new Error(base + ": path count changed while copying");
    var items = [], keys = [];
    for (var r = 0; r < doc.pathItems.length; r++) if (cols[r]) { items.push(doc.pathItems[r]); keys.push(cols[r]); }
    cols = keys;
    for (var q = 0; q < items.length; q++) {
      var m = MAP[cols[q]];
      if (!m) { miss.push(base + ":" + cols[q]); continue; }
      items[q].fillColor = cmyk(m);
    }
    doc.saveAs(new File(ROOT + "/CMYK/AI/" + base + ".ai"), ai);
    var eps = new EPSSaveOptions();
    eps.compatibility = Compatibility.ILLUSTRATOR8;      // AI10+ embeds private editing data (~0.8 MB/file)
    eps.embedAllFonts = false; eps.preview = EPSPreview.None; eps.includeDocumentThumbnails = false;
    doc.saveAs(new File(ROOT + "/CMYK/EPS/" + base + ".eps"), eps);
    var cp = new PDFSaveOptions(); cp.pDFPreset = "[PDF/X-1a:2001]";
    doc.saveAs(new File(ROOT + "/CMYK/PDF/" + base + ".pdf"), cp);
    var back = items.length ? items[0].fillColor : null;           // read it back: assignment can fail silently
    if (!back || back.typename != "CMYKColor") throw new Error(base + ": fill is not CMYK after assignment");
    log.push(base + " | recolored " + items.length);
    doc.close(SaveOptions.DONOTSAVECHANGES);
  }
  app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;
  return log.join("\n") + "\nUNMAPPED: " + (miss.length ? miss.join(", ") : "none");
})();
