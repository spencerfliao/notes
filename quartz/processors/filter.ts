// import { BuildCtx } from "../util/ctx"
// import { PerfTimer } from "../util/perf"
// import { ProcessedContent } from "../plugins/vfile"

// export function filterContent(ctx: BuildCtx, content: ProcessedContent[]): ProcessedContent[] {
//   const { cfg, argv } = ctx
//   const perf = new PerfTimer()
//   const initialLength = content.length
//   for (const plugin of cfg.plugins.filters) {
//     const updatedContent = content.filter((item) => plugin.shouldPublish(ctx, item))

//     if (argv.verbose) {
//       const diff = content.filter((x) => !updatedContent.includes(x))
//       for (const file of diff) {
//         console.log(`[filter:${plugin.name}] ${file[1].data.slug}`)
//       }
//     }

//     content = updatedContent
//   }

//   console.log(`Filtered out ${initialLength - content.length} files in ${perf.timeSince()}`)
//   return content
// }

import { BuildCtx } from "../util/ctx"
import { PerfTimer } from "../util/perf"
import { ProcessedContent } from "../plugins/vfile"

export function filterContent(ctx: BuildCtx, content: ProcessedContent[]): ProcessedContent[] {
  const { cfg, argv } = ctx
  const perf = new PerfTimer()
  const initialLength = content.length

  for (const plugin of cfg.plugins.filters) {
    let updatedContent = content.filter((item) => plugin.shouldPublish(ctx, item))

    // Exclude everything inside the "private/" folder from being listed
    updatedContent = updatedContent.filter((item) => {
      const slug = item[1].data.slug || ""
      return !slug.startsWith("private/") // Hide "private/" folder content
    })

    if (argv.verbose) {
      const diff = content.filter((x) => !updatedContent.includes(x))
      for (const file of diff) {
        console.log(`[filter:${plugin.name}] ${file[1].data.slug}`)
      }
    }

    content = updatedContent
  }

  console.log(`Filtered out ${initialLength - content.length} files in ${perf.timeSince()}`)
  return content
}
