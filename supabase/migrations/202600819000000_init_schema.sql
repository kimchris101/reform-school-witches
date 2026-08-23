-- Migration: 20260819000000_init_schema.sql
-- Description: Complete schema for Our Lady of Tears Academy Reader Portal

-- Enable UUID Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Profiles Table
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    alias TEXT NOT NULL,
    archetype TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    last_active TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Quiz Submissions
CREATE TABLE IF NOT EXISTS public.quiz_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE,
    answers JSONB NOT NULL,
    scores JSONB NOT NULL,
    assigned_archetype TEXT NOT NULL,
    diocesan_seal_code TEXT UNIQUE NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Character Dossiers
CREATE TABLE IF NOT EXISTS public.character_dossiers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    full_name TEXT NOT NULL,
    alias TEXT,
    patron_saint TEXT NOT NULL,
    sacramental_affinity TEXT NOT NULL,
    classification_class TEXT NOT NULL,
    biography TEXT NOT NULL,
    key_quotes TEXT[] DEFAULT '{}',
    portrait_url TEXT NOT NULL,
    voice_sample_url TEXT,
    is_spoiler BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Media Unlocks Catalog
CREATE TABLE IF NOT EXISTS public.media_unlocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    node_trigger_id TEXT UNIQUE NOT NULL,
    video_url TEXT NOT NULL,
    thumbnail_url TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 5. User Progress & Unlocks Junction
CREATE TABLE IF NOT EXISTS public.user_progress (
    profile_id UUID PRIMARY KEY REFERENCES public.profiles(id) ON DELETE CASCADE,
    unlocked_nodes TEXT[] DEFAULT '{}',
    unlocked_media_ids UUID[] DEFAULT '{}',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quiz_submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.character_dossiers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.media_unlocks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_progress ENABLE ROW LEVEL SECURITY;

-- Public Read Policies
CREATE POLICY "Public dossiers are viewable by anyone" ON public.character_dossiers FOR SELECT USING (true);
CREATE POLICY "Public media triggers are viewable by anyone" ON public.media_unlocks FOR SELECT USING (true);

-- Seed Initial Character Dossier Records
INSERT INTO public.character_dossiers (
    slug, full_name, alias, patron_saint, sacramental_affinity, classification_class, biography, key_quotes, portrait_url, is_spoiler
) VALUES 
(
    'roman-de-la-croix', 
    'Roman De La Croix', 
    'The Co-Link Conduit', 
    'St. Michael the Archangel', 
    'Symphonic Resonance & Sacramental Steel', 
    'High Rite Shield / Perimeter Marshal', 
    'Forged in the crucible of the New Orleans Diocesan Tribunal, Roman acts as the primary anchor for High Rite exorcisms. His soul operates as a high-capacity conduit, capable of interlocking spiritual frequencies with a partner to form an unbreakable barrier against demonic broadcast signals.', 
    ARRAY['Two heartbeats, one circuit. The dark cannot break what is held in common.', 'Keep your feet in the salt and your eyes on the altar.'], 
    '/static/media/dossiers/roman.jpg', 
    FALSE
),
(
    'kimbra-woods', 
    'Kimbra Woods', 
    'The Chalice', 
    'The Blessed Virgin Mary', 
    'Consecrated Light & Unbroken Vessels', 
    'Consecrated Vessel / Exception', 
    'Sold to the Crimson Root as a child due to her uncorrupted spiritual purity, Kimbra was intended to serve as a power source for an ancestral blood debt. Sealed by the Sacrament at Our Lady of Tears Academy, she has been gifted a raw holy illumination, serving as the flame around which the Academy''s perimeter walls are sustained.', 
    ARRAY['They tried to turn my heart into a battery. They forgot that Light consumes the wires.', 'My interior doors remain locked.'], 
    '/static/media/dossiers/kimbra.jpg', 
    FALSE
),
(
    'genesis', 
    'Genesis', 
    'The Sonic Scrambler', 
    'St. Cecilia', 
    'Acoustic Dissonance & Signal Interruption', 
    'Tactical Disruptor / Free Conduits', 
    'A prodigal daughter of the Catholic Church, dabbled in the occult and was left screaming in a mental health facility. The Rector, Father Manuel and his team exorcised the demon afflicting her and she chose to enter the Academy for reform. As a fractured frequency she learned to scramble the enemy''s signal.', 
    ARRAY['If they cannot lock onto your frequency, they cannot harvest your marrow.', 'Noise is just a prayer that has not found its cadence yet.'], 
    '/static/media/dossiers/genesis.jpg', 
    FALSE
)
(
    'ignatius-santiago', 
    'Ignatius Santiago', 
    'The Sentinel Shield', 
    'St. James the Greater', 
    'Granite Density & Sacramental Fortification', 
    'Perimeter Guard / Penitent Sentry', 
    'Standing guard at the outer salt line where the swamp meets the academy stone, Ignatius absorbs the physical discharge of malignant entities. Carrying an immense weight of penance, his body acts as a literal anvil, grounding lethal energetic strikes before they reach the inner courtyard.', 
    ARRAY['Let the swamp take my boots before it touches the sanctuary.', 'Stand firm. The salt does not yield.'], 
    '/static/media/dossiers/ignatius.jpg', 
    FALSE
)
ON CONFLICT (slug) DO NOTHING;