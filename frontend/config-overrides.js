// Overriding CreateReactApp settings, ref: https://github.com/arackaf/customize-cra
// const antdTheme = require("./src/theme.js");
const {
  override,
  fixBabelImports,
  // useEslintRc,
  // addLessLoader,
  addDecoratorsLegacy
} = require("customize-cra");

module.exports = override(
  addDecoratorsLegacy(),
  // useEslintRc(),
  fixBabelImports("import"),
  // addLessLoader({
  //   javascriptEnabled: true,
  //   modifyVars: antdTheme
  // })
);
