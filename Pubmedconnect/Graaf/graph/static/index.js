
         t = new NetChart({
            container: document.getElementById("graph"),
            area: { height: 300 },
            data: {src: "Pubmedconnect/static/dataaa.json"},
            navigation: {
                mode: "showall"
            },
            style: {
                link: { fillColor: "limegreen" },
                node: { imageCropping: true},
                nodeStyleFunction: nodeStyle
            },
            interaction: { rotation: {fingers: true}}
        });
        function nodeStyle(node) {
            node.label = node.data.name;
        }