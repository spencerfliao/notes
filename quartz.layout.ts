import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      Home: "https://spencereads.com"
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    Component.DesktopOnly(Component.Explorer()),
  ],
  right: [
    Component.Graph({
      localGraph: {
        drag: true,
        zoom: true,
        depth: 1, // Show up to 2 hops for more connections
        scale: 1.5, // Slightly zoomed in for better clarity
        repelForce: 0.7, // More spacing between nodes
        centerForce: 0.5, // Stronger pull toward the center
        linkDistance: 50, // Spread nodes further apart
        fontSize: 0.5, // Larger node labels
        opacityScale: 0.8, // Labels fade out more slowly
        removeTags: [], // No tags removed
        showTags: false, // Show tags in the graph
        enableRadial: false, // Constrain to a radial layout
      },
      globalGraph: {
        drag: true,
        zoom: true,
        depth: -1, // Unlimited depth for global graphs
        scale: 1.2, // Slightly zoomed out for global clarity
        repelForce: 0.5, // More spacing for global view
        centerForce: 0.5, // Keep global graph focused
        linkDistance: 50, // Spread nodes further apart
        fontSize: 0.5, // Larger labels for global view
        opacityScale: 0.5, // Labels fade out more slowly
        removeTags: [], // No tags removed
        showTags: false, // Show tags in global graph
        enableRadial: false, // Constrain global graph to a radial layout
      },    
    }),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    Component.DesktopOnly(Component.Explorer()),
  ],
  right: [],
}
