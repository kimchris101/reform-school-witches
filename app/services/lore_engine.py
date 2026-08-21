from typing import List, Dict, Optional

# Canonical Lore Registry extracted from The Blood Lily Contract
LORE_REGISTRY: List[Dict[str, str]] = [
    {
        "topic": "sanguine_tether",
        "keywords": "tether, link, wire, siphoning, hearth, graft, droit de greffe",
        "canon_context": (
            "The Sanguine Tether is a 300-year-old parasitic link created by the Boudreaux family. "
            "A designated Hearth (biological battery, such as Kimbra Woods) is branded with a Blood Lily iron mark[cite: 1]. "
            "This allows the heir (Damian) to siphon her life-force to sustain his defective physical body and extend their dynasty[cite: 1]."
        )
    },
    {
        "topic": "emergency_baptism",
        "keywords": "baptism, water, seal, chrism, confirmed, mary, renunciation",
        "canon_context": (
            "Father Manuel performed an emergency Baptism on Kimberly Woods in the White Room while Roman grounded the static[cite: 1]. "
            "By renouncing Satan, the Crimson Root, and Damian Boudreaux, her un-owned status was overwritten[cite: 1]. "
            "The Baptism severed the Sanguine Tether, transforming her scar into sterling silver and rendering her an official Citizen of the Kingdom[cite: 1]."
        )
    },
    {
        "topic": "one_soul_colink",
        "keywords": "co-link, colink, one soul, shield, chalice, sponsor, ground, eucharist",
        "canon_context": (
            "The Doctrine of the One Soul dictates that a Shield (Roman) and a Chalice (Kimbra/Mary) form a sacramental circuit[cite: 1]. "
            "The Shield acts as an anvil/ground to absorb supernatural feedback, while the Chalice projects the divine Presence fed by the Eucharist[cite: 1]. "
            "When two become one in Christ's Name, they restore order rather than scramble the air[cite: 1]."
        )
    },
    {
        "topic": "our_lady_of_tears",
        "keywords": "academy, tears, crown of tears, salt, sanctuary lamp, north tower, exceptions",
        "canon_context": (
            "Our Lady of Tears Academy is a fortress of salt and stone in Louisiana established in 1833[cite: 1]. "
            "It trains Exceptions—souls burdened by demonic afflictions—as holy soldiers[cite: 1]. "
            "Defenses rely on consecrated salt lines, moat brine, the Crown of Tears Rosary (49 white beads), and Perpetual Adoration[cite: 1]."
        )
    },
    {
        "topic": "crimson_root",
        "keywords": "root, vincent, boudreaux, ledger, debt, livre de la racine, proxy",
        "canon_context": (
            "The Crimson Root is the occult system governed by Vincent Boudreaux using the Livre de la Racine (Ledger of Debts)[cite: 1]. "
            "It operates under the Petit Catéchisme, treating unsealed human souls as biological assets[cite: 1]. "
            "When Kimbra's tether snapped, Vincent used a secondary Proxy girl to temporarily supply Damian with stolen vitality[cite: 1]."
        )
    }
]

def retrieve_lore_context(query: str) -> str:
    """Searches canonical lore registry for matching topics based on query keywords."""
    query_lower = query.lower()
    matched_contexts = []
    
    for entry in LORE_REGISTRY:
        keywords = [k.strip() for k in entry["keywords"].split(",")]
        if any(keyword in query_lower for keyword in keywords):
            matched_contexts.append(entry["canon_context"])
            
    if not matched_contexts:
        return "No specific manuscript lore matched, rely strictly on core character system prompt."
        
    return "\n\n".join(matched_contexts)