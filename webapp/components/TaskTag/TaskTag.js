export default function TaskTag({type = "", severity = ""}) {
    const severityDict = {
        "high": {
            text: "Alto",
            chip: "critical"
        },
        "medium": {
            text: "Medio",
            chip: "warning"
        },
        "low": {
            text: "Bajo",
            chip: "low"
        },
        "information": {
            text: "Informativo",
            chip: "info"
        },
        "recommendation": {
            text: "Informativo",
            chip: "info"
        }
    }

    return (
        <>
        { type !== "" && (
        <span className="chip chip--type">
            <span className="chip-text">{type}</span>
        </span>
        )}
        { severity !== "" && (
        <span className={`chip chip--${severityDict[severity.toLowerCase()].chip}`}>
            <span className="chip-text">{severityDict[severity.toLowerCase()].text}</span>
        </span>
        )}
        </>
    )
}