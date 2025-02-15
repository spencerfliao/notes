import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types";
import explorerStyle from "./styles/explorer.scss";

// @ts-ignore
import script from "./scripts/explorer.inline";
import { ExplorerNode, FileNode, Options } from "./ExplorerNode";
import { QuartzPluginData } from "../plugins/vfile";
import { classNames } from "../util/lang";
import { i18n } from "../i18n";

const defaultOptions = {
  folderClickBehavior: "collapse",
  folderDefaultState: "collapsed",
  useSavedState: true,
  mapFn: (node) => node,
  sortFn: (a, b) => {
    if ((!a.file && !b.file) || (a.file && b.file)) {
      return a.displayName.localeCompare(b.displayName, undefined, { numeric: true, sensitivity: "base" });
    }
    return a.file && !b.file ? 1 : -1;
  },
  filterFn: (node) => node.name !== "tags",
  order: ["filter", "map", "sort"],
} satisfies Options;

export default ((userOpts?: Partial<Options>) => {
  const opts: Options = { ...defaultOptions, ...userOpts };

  let fileTree: FileNode;
  let jsonTree: string;

  function constructFileTree(allFiles: QuartzPluginData[]) {
    if (fileTree) return;
    fileTree = new FileNode("");
    allFiles.forEach((file) => fileTree.add(file));
    if (opts.order) {
      opts.order.forEach((fn) => {
        if (fn === "map") fileTree.map(opts.mapFn);
        if (fn === "sort") fileTree.sort(opts.sortFn);
        if (fn === "filter") fileTree.filter(opts.filterFn);
      });
    }
    const folders = fileTree.getFolderPaths(opts.folderDefaultState === "collapsed");
    jsonTree = JSON.stringify(folders);
  }

  function toggleExplorer() {
    const explorer = document.getElementById("explorer-content");
    if (explorer) {
      explorer.classList.toggle("collapsed");
    }
  }

  const Explorer: QuartzComponent = ({ ctx, cfg, allFiles, displayClass, fileData }: QuartzComponentProps) => {
    constructFileTree(allFiles);
    
    return (
      <div class={classNames(displayClass, "explorer")}>
        {displayClass === "mobile-only" && (
          <button type="button" id="explorer-toggle" class="burger-button" onClick={toggleExplorer}>
            <svg width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu">
              <line x1="4" x2="20" y1="12" y2="12" />
              <line x1="4" x2="20" y1="6" y2="6" />
              <line x1="4" x2="20" y1="18" y2="18" />
            </svg>
          </button>
        )}
        <button type="button" id="explorer" data-behavior={opts.folderClickBehavior} data-collapsed={opts.folderDefaultState} data-savestate={opts.useSavedState} data-tree={jsonTree}>
          <h2>{opts.title ?? i18n(cfg.locale).components.explorer.title}</h2>
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="5 8 14 8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="fold">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </button>
        <div id="explorer-content" class="collapsed">
          <ul class="overflow" id="explorer-ul">
            <ExplorerNode node={fileTree} opts={opts} fileData={fileData} />
            <li id="explorer-end" />
          </ul>
        </div>
      </div>
    );
  };

  Explorer.css = explorerStyle;
  Explorer.afterDOMLoaded = script;
  return Explorer;
}) satisfies QuartzComponentConstructor;
