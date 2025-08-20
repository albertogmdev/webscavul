import { useEffect, useState } from "react"
import prettier from "prettier/standalone"
import * as htmlParser from 'prettier/parser-html'

export default function Code({ html }) {
    const [code, setCode] = useState("")

    useEffect(() => {
        const htmlDecode = (htmlCode) => {
            const doc = new DOMParser().parseFromString(htmlCode, "text/html");
            return doc.documentElement.textContent;
        }

        if (html) {
            const decodedHtml = htmlDecode(html)
            const formatted = prettier.format(decodedHtml, {
                parser: "html",
                plugins: [htmlParser],
                useTabs: true,
                bracketSameLine: true,
                tabWidth: 1,
            })

            setCode(formatted)
        }
    }, [html])

    return <pre>{code}</pre>
}
