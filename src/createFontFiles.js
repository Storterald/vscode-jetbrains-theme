const webfont = require('webfont');
const fs = require('fs');
const path = require('path');
const glob = require('glob');

const startUnicode = 0xE000;
const iconDefinitions = {};
const jsonContent = {
        fonts: [
                {
                        id: "jetbrains-new-ui-product-icons",
                        src: [
                                {
                                        path: "./product-icons.woff",
                                        format: "woff",
                                },
                        ],
                        weight: "normal",
                        style: "normal",
                },
        ],
        iconDefinitions
};

async function generateFont(color) {
        try {
                const svgsPath = path.join(__dirname, "..", "resources", "product", "*.svg").replace(/\\/g, '/');
                const svgs = glob.sync(svgsPath).reverse();
                
                let unicodeValue = startUnicode;
                svgs.forEach((svg) => {
                        iconDefinitions[path.basename(svg, ".svg")] = {
                                fontCharacter: `\\${unicodeValue.toString(16).toUpperCase()}`
                        };

                        unicodeValue++;
                });
                
                const jsonDest = path.join(__dirname, "..", "icons", "product-icon-theme.json");
                fs.writeFileSync(jsonDest, JSON.stringify(jsonContent, null, 2), 'utf-8');

                const result = await webfont.webfont({
                        files: svgsPath,
                        formats: ['woff'],
                        startUnicode: startUnicode,
                        verbose: true,
                        normalize: true,
                        sort: false
                });

                const woffDest = path.join(__dirname, "..", "icons", "product-icons.woff");
                fs.writeFileSync(woffDest, result.woff, "binary");
        } catch (e) {
                return Promise.reject(new Error(e));
        }
}

generateFont().then(() => { }, (e) => { throw e; });