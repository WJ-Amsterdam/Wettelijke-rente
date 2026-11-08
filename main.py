import asyncio
from typing import Annotated

from pydantic import Field
from mistralai import agents

from rente import bereken_wettelijke_rente as _bereken


@agents.tool
def bereken_wettelijke_rente(
    bedrag: Annotated[float, Field(description="Hoofdsom in euro's waarover rente wordt berekend.")],
    startdatum: Annotated[str, Field(description="Startdatum van de renteperiode, formaat YYYY-MM-DD.")],
    einddatum: Annotated[str, Field(description="Einddatum van de renteperiode, formaat YYYY-MM-DD.")],
) -> dict:
    """Bereken de wettelijke rente voor NIET-handelstransacties (art. 6:119 BW) over een bedrag
    van startdatum tot en met einddatum. Geeft een per-periode overzicht terug."""
    try:
        return _bereken(bedrag, startdatum, einddatum)
    except ValueError as exc:
        raise agents.ToolError(str(exc))


agent = agents.Agent(
    model="mistral-large-4",
    name="wettelijke-rente-agent",
    instructions=(
        "Je bent een Nederlandse juridisch-financiele assistent. Bereken de wettelijke rente "
        "voor niet-handelstransacties (art. 6:119 BW) met de tool bereken_wettelijke_rente. "
        "Vraag om bedrag, startdatum en einddatum als die ontbreken. "
        "Toon altijd het per-periode overzicht dat de tool teruggeeft: per renteperiode de "
        "datums, het aantal dagen, het percentage en het rentebedrag, plus het totaal. "
        "Vermeld dat het om enkelvoudige rente per dag gaat (bedrag x rente% / 365). "
        "Antwoord in het Nederlands."
    ),
    tools=[bereken_wettelijke_rente],
)


async def main() -> None:
    result = await agent.run("Bereken de wettelijke rente over 10000 euro van 2025-03-01 tot 2026-06-30.")
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())