# Compatibility

The extension edits colors of the following extensions: ***GitHub Pull Requests and Issues***, ***Geode***.

## Updates

The extension is frequently updated to add further support of keywords and languages.

## Other Extensions and addons

It's suggested to also use the ***JetBrains Icon Theme*** extension and the ***JetBrains Mono*** font. Furthermore you could use the ***Better Comments*** extension and replace the setting.json part with:

<pre>
"better-comments.tags": [  
    {  
        "tag": "TODO",
        "color": "#8bb33d",
        "strikethrough": false,
        "underline": false,
        "backgroundColor": "transparent",
        "bold": false,
        "italic": true
    }
]
</pre>

to add something similar to the ***TODO()***, *it will still require to be inside a comment*
