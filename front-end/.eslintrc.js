module.exports = {
    "env": {
        "browser": true,
        "commonjs": true,
        "es6": true,
        "node": true,
        "meteor": true
    },
    "extends": "eslint:recommended",
    "parserOptions": {
        "sourceType": "module"
    },
    "rules": {
        "indent": [
            "error",
            2
        ],
        "linebreak-style": [
            "error",
            "unix"
        ],
        "quotes": [
            "error",
            "single",
            {
              "allowTemplateLiterals": true
            }
        ],
        "semi": [
            "error",
            "always"
        ],
        "no-console": 0,
        "no-unused-vars": [
          "error", 
          { "argsIgnorePattern": "^_" }
        ]
    },
    "globals": {
        "Iron": true,
        "jQuery": true,
        "d3Graph": true,
        "d3": true,
        "$": true,
        "toastr": true,
        "google": true,
        "moment": true,
        "WOW": true,
    }
};
