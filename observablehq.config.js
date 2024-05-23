// See https://observablehq.com/framework/config for documentation.
export default {
  title: "Tilt-Corrected BF-STEM (Parallax) Imaging",

  // The pages and sections in the sidebar. If you don’t specify this option,
  // all pages will be listed in alphabetical order. Listing pages explicitly
  // lets you organize them into sections and have unlisted pages.
  // pages: [
  //   {
  //     name: "Examples",
  //     pages: [
  //       {name: "Dashboard", path: "/example-dashboard"},
  //       {name: "Report", path: "/example-report"}
  //     ]
  //   }
  // ],

  head: '<link rel="icon" href="observable.png" type="image/png" sizes="32x32">',
  root: "src",
  pages: [
    {name: "Phase Problem", path: "phase-problem"},
    {name: "Ray Diagrams", path: "ray-diagrams"},
    {name: "TEM/STEM Reciprocity", path: "reciprocity"},
    {name: "Tilt-Corrected BF-STEM", path: "parallax"},
    {name: "Phase Retrieval in py4DSTEM", path: "py4dstem"},
  ],
  theme: "light",
};
