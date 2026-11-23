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

    // CMYK: remember each path's RGB, switch document mode, then assign the specified values
    var items = [], cols = [];
    for (var p = 0; p < doc.pathItems.length; p++) {
      var it = doc.pathItems[p];
      if (it.filled && it.fillColor.typename == "RGBColor") { items.push(it); cols.push(hex(it.fillColor)); }
    }
    app.executeMenuCommand("doc-color-cmyk");
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
    doc.saveAs(new File(ROOT + "/CMYK/PDF/" + base + ".pdf"), pdf);
    log.push(base + " | recolored " + items.length);
    doc.close(SaveOptions.DONOTSAVECHANGES);
  }
  app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS;
  return log.join("\n") + "\nUNMAPPED: " + (miss.length ? miss.join(", ") : "none");
})();
