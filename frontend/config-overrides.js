module.exports = function override(config) {
    config.module.rules = config.module.rules.map((rule) => {
      if (rule.loader && rule.loader.includes('source-map-loader')) {
        return {
          ...rule,
          exclude: /@mediapipe/,
        };
      }
      return rule;
    });
    return config;
  };