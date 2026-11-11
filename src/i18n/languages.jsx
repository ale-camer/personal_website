import React from 'react';

export const LANGUAGES = [
  {
    code: 'ES',
    nativeName: 'Español',
    name: 'Spanish',
    region: 'Argentina • España • LatAm',
    flag: 'ES',
    flagSpec: { type: 'h3', colors: ['#AA151B', '#F1BF00', '#AA151B'] }
  },
  {
    code: 'EN',
    nativeName: 'English',
    name: 'English',
    region: 'United States • UK',
    flag: 'US',
    flagSpec: { type: 'us', colors: ['#B22234', '#FFFFFF', '#3C3B6E'] }
  },
  {
    code: 'PT',
    nativeName: 'Português',
    name: 'Portuguese',
    region: 'Brasil • Portugal',
    flag: 'BR',
    flagSpec: { type: 'br', colors: ['#009B3A', '#FEDF00', '#002776'] }
  },
  {
    code: 'FR',
    nativeName: 'Français',
    name: 'French',
    region: 'France • Suisse',
    flag: 'FR',
    flagSpec: { type: 'v3', colors: ['#002395', '#FFFFFF', '#ED2939'] }
  },
  {
    code: 'DE',
    nativeName: 'Deutsch',
    name: 'German',
    region: 'Deutschland • DACH',
    flag: 'DE',
    flagSpec: { type: 'h3', colors: ['#000000', '#DD0000', '#FFCE00'] }
  },
  {
    code: 'IT',
    nativeName: 'Italiano',
    name: 'Italian',
    region: 'Italia • Svizzera',
    flag: 'IT',
    flagSpec: { type: 'v3', colors: ['#009246', '#FFFFFF', '#CE2B37'] }
  },
  {
    code: 'NL',
    nativeName: 'Nederlands',
    name: 'Dutch',
    region: 'Nederland • België',
    flag: 'NL',
    flagSpec: { type: 'h3', colors: ['#AE1C28', '#FFFFFF', '#21468B'] }
  },
  {
    code: 'PL',
    nativeName: 'Polski',
    name: 'Polish',
    region: 'Polska • Warsaw',
    flag: 'PL',
    flagSpec: { type: 'h2', colors: ['#FFFFFF', '#DC143C'] }
  },
  {
    code: 'SV',
    nativeName: 'Svenska',
    name: 'Swedish',
    region: 'Sverige • Stockholm',
    flag: 'SE',
    flagSpec: { type: 'cross', colors: ['#006AA7', '#FECC02'] }
  },
  {
    code: 'NO',
    nativeName: 'Norsk',
    name: 'Norwegian',
    region: 'Norge • Oslo',
    flag: 'NO',
    flagSpec: { type: 'cross', colors: ['#BA0C2F', '#00205B'] }
  },
  {
    code: 'DA',
    nativeName: 'Dansk',
    name: 'Danish',
    region: 'Danmark • Copenhagen',
    flag: 'DK',
    flagSpec: { type: 'cross', colors: ['#C8102E', '#FFFFFF'] }
  },
  {
    code: 'FI',
    nativeName: 'Suomi',
    name: 'Finnish',
    region: 'Suomi • Helsinki',
    flag: 'FI',
    flagSpec: { type: 'cross', colors: ['#FFFFFF', '#003580'] }
  },
  {
    code: 'IS',
    nativeName: 'Íslenska',
    name: 'Icelandic',
    region: 'Ísland • Reykjavík',
    flag: 'IS',
    flagSpec: { type: 'cross', colors: ['#02529C', '#DC1E35'] }
  },
  {
    code: 'CS',
    nativeName: 'Čeština',
    name: 'Czech',
    region: 'Česko • Prague',
    flag: 'CZ',
    flagSpec: { type: 'h2', colors: ['#FFFFFF', '#D7141A'] }
  },
  {
    code: 'SK',
    nativeName: 'Slovenčina',
    name: 'Slovak',
    region: 'Slovensko • Bratislava',
    flag: 'SK',
    flagSpec: { type: 'h3', colors: ['#FFFFFF', '#0B4EA2', '#EE1C25'] }
  },
  {
    code: 'HU',
    nativeName: 'Magyar',
    name: 'Hungarian',
    region: 'Magyarország • Budapest',
    flag: 'HU',
    flagSpec: { type: 'h3', colors: ['#CE2939', '#FFFFFF', '#477050'] }
  },
  {
    code: 'RO',
    nativeName: 'Română',
    name: 'Romanian',
    region: 'România • Bucharest',
    flag: 'RO',
    flagSpec: { type: 'v3', colors: ['#002B7F', '#FCD116', '#CE1126'] }
  },
  {
    code: 'BG',
    nativeName: 'Български',
    name: 'Bulgarian',
    region: 'България • Sofia',
    flag: 'BG',
    flagSpec: { type: 'h3', colors: ['#FFFFFF', '#00966E', '#D62612'] }
  },
  {
    code: 'EL',
    nativeName: 'Ελληνικά',
    name: 'Greek',
    region: 'Ελλάδα • Athens',
    flag: 'GR',
    flagSpec: { type: 'h3', colors: ['#0D5EAF', '#FFFFFF', '#0D5EAF'] }
  },
  {
    code: 'TR',
    nativeName: 'Türkçe',
    name: 'Turkish',
    region: 'Türkiye • Istanbul',
    flag: 'TR',
    flagSpec: { type: 'circle', colors: ['#E30A17', '#FFFFFF'] }
  },
  {
    code: 'RU',
    nativeName: 'Русский',
    name: 'Russian',
    region: 'Россия • CIS',
    flag: 'RU',
    flagSpec: { type: 'h3', colors: ['#FFFFFF', '#0039A6', '#D52B1E'] }
  },
  {
    code: 'UK',
    nativeName: 'Українська',
    name: 'Ukrainian',
    region: 'Україна • Kyiv',
    flag: 'UA',
    flagSpec: { type: 'h2', colors: ['#0057B7', '#FFDD00'] }
  },
  {
    code: 'SR',
    nativeName: 'Српски',
    name: 'Serbian',
    region: 'Србија • Belgrade',
    flag: 'RS',
    flagSpec: { type: 'h3', colors: ['#C6363C', '#0C4076', '#FFFFFF'] }
  },
  {
    code: 'HR',
    nativeName: 'Hrvatski',
    name: 'Croatian',
    region: 'Hrvatska • Zagreb',
    flag: 'HR',
    flagSpec: { type: 'h3', colors: ['#FF0000', '#FFFFFF', '#171796'] }
  },
  {
    code: 'SL',
    nativeName: 'Slovenščina',
    name: 'Slovenian',
    region: 'Slovenija • Ljubljana',
    flag: 'SI',
    flagSpec: { type: 'h3', colors: ['#FFFFFF', '#005CE6', '#FF0000'] }
  },
  {
    code: 'LT',
    nativeName: 'Lietuvių',
    name: 'Lithuanian',
    region: 'Lietuva • Vilnius',
    flag: 'LT',
    flagSpec: { type: 'h3', colors: ['#FDB913', '#006A44', '#C1272D'] }
  },
  {
    code: 'LV',
    nativeName: 'Latviešu',
    name: 'Latvian',
    region: 'Latvija • Riga',
    flag: 'LV',
    flagSpec: { type: 'h3', colors: ['#9E3039', '#FFFFFF', '#9E3039'] }
  },
  {
    code: 'ET',
    nativeName: 'Eesti',
    name: 'Estonian',
    region: 'Eesti • Tallinn',
    flag: 'EE',
    flagSpec: { type: 'h3', colors: ['#0072CE', '#000000', '#FFFFFF'] }
  },
  {
    code: 'GA',
    nativeName: 'Gaeilge',
    name: 'Irish',
    region: 'Éire • Dublin',
    flag: 'IE',
    flagSpec: { type: 'v3', colors: ['#169B62', '#FFFFFF', '#FF883E'] }
  },
  {
    code: 'CA',
    nativeName: 'Català',
    name: 'Catalan',
    region: 'Catalunya • Andorra',
    flag: 'CA',
    flagSpec: { type: 'h3', colors: ['#FCDD09', '#DA121A', '#FCDD09'] }
  },
  {
    code: 'EU',
    nativeName: 'Euskara',
    name: 'Basque',
    region: 'Euskadi • Bilbao',
    flag: 'EU',
    flagSpec: { type: 'cross', colors: ['#D52B1E', '#009B48'] }
  },
  {
    code: 'GL',
    nativeName: 'Galego',
    name: 'Galician',
    region: 'Galicia • A Coruña',
    flag: 'GL',
    flagSpec: { type: 'h2', colors: ['#FFFFFF', '#0099CC'] }
  },
  {
    code: 'AR',
    nativeName: 'العربية',
    name: 'Arabic',
    region: 'MENA • Riyadh / Dubai',
    flag: 'AE',
    flagSpec: { type: 'h3', colors: ['#007A3D', '#FFFFFF', '#000000'] }
  },
  {
    code: 'HE',
    nativeName: 'עברית',
    name: 'Hebrew',
    region: 'ישראל • Tel Aviv',
    flag: 'IL',
    flagSpec: { type: 'h3', colors: ['#0038B8', '#FFFFFF', '#0038B8'] }
  },
  {
    code: 'FA',
    nativeName: 'فارسی',
    name: 'Persian',
    region: 'ایران • Tehran',
    flag: 'IR',
    flagSpec: { type: 'h3', colors: ['#239F40', '#FFFFFF', '#DA0000'] }
  },
  {
    code: 'UR',
    nativeName: 'اردو',
    name: 'Urdu',
    region: 'پاکستان • Karachi',
    flag: 'PK',
    flagSpec: { type: 'circle', colors: ['#01411C', '#FFFFFF'] }
  },
  {
    code: 'HI',
    nativeName: 'हिन्दी',
    name: 'Hindi',
    region: 'भारत • Mumbai / NSE',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'BN',
    nativeName: 'বাংলা',
    name: 'Bengali',
    region: 'বাংলাদেশ • Dhaka / Kolkata',
    flag: 'BD',
    flagSpec: { type: 'circle', colors: ['#006A4E', '#F42A41'] }
  },
  {
    code: 'PA',
    nativeName: 'ਪੰਜਾਬੀ',
    name: 'Punjabi',
    region: 'ਪੰਜਾਬ • Punjab',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'TA',
    nativeName: 'தமிழ்',
    name: 'Tamil',
    region: 'தமிழ்நாடு • Chennai / SG',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'TE',
    nativeName: 'తెలుగు',
    name: 'Telugu',
    region: 'హైదరాబాద్ • Hyderabad',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'MR',
    nativeName: 'मराठी',
    name: 'Marathi',
    region: 'महाराष्ट्र • Mumbai',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'GU',
    nativeName: 'ગુજરાતી',
    name: 'Gujarati',
    region: 'ગુજરાત • GIFT City',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'KN',
    nativeName: 'ಕನ್ನಡ',
    name: 'Kannada',
    region: 'ಕರ್ನಾಟಕ • Bengaluru',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'ML',
    nativeName: 'മലയാളം',
    name: 'Malayalam',
    region: 'കേരളം • Kochi',
    flag: 'IN',
    flagSpec: { type: 'h3', colors: ['#FF9933', '#FFFFFF', '#138808'] }
  },
  {
    code: 'TH',
    nativeName: 'ไทย',
    name: 'Thai',
    region: 'ประเทศไทย • Bangkok',
    flag: 'TH',
    flagSpec: { type: 'h3', colors: ['#A51931', '#2D2A4A', '#A51931'] }
  },
  {
    code: 'VI',
    nativeName: 'Tiếng Việt',
    name: 'Vietnamese',
    region: 'Việt Nam • Ho Chi Minh',
    flag: 'VN',
    flagSpec: { type: 'circle', colors: ['#DA251D', '#FFFF00'] }
  },
  {
    code: 'ID',
    nativeName: 'Bahasa Indonesia',
    name: 'Indonesian',
    region: 'Indonesia • Jakarta',
    flag: 'ID',
    flagSpec: { type: 'h2', colors: ['#FF0000', '#FFFFFF'] }
  },
  {
    code: 'MS',
    nativeName: 'Bahasa Melayu',
    name: 'Malay',
    region: 'Malaysia • Kuala Lumpur',
    flag: 'MY',
    flagSpec: { type: 'h3', colors: ['#CC0001', '#010066', '#FFCC00'] }
  },
  {
    code: 'TL',
    nativeName: 'Filipino',
    name: 'Filipino / Tagalog',
    region: 'Pilipinas • Manila',
    flag: 'PH',
    flagSpec: { type: 'h2', colors: ['#0038A8', '#CE1126'] }
  },
  {
    code: 'JA',
    nativeName: '日本語',
    name: 'Japanese',
    region: '日本 • Tokyo',
    flag: 'JP',
    flagSpec: { type: 'circle', colors: ['#FFFFFF', '#BC002D'] }
  },
  {
    code: 'KO',
    nativeName: '한국어',
    name: 'Korean',
    region: '대한민국 • Seoul',
    flag: 'KR',
    flagSpec: { type: 'circle', colors: ['#FFFFFF', '#CD2E3A'] }
  },
  {
    code: 'ZH',
    nativeName: '中文 (简体)',
    name: 'Chinese (Simplified)',
    region: '中国 • Shanghai / Shenzhen',
    flag: 'CN',
    flagSpec: { type: 'circle', colors: ['#DE2910', '#FFDE00'] }
  },
  {
    code: 'ZH-TW',
    nativeName: '中文 (繁體)',
    name: 'Chinese (Traditional)',
    region: '台灣 • Taipei / Hong Kong',
    flag: 'TW',
    flagSpec: { type: 'circle', colors: ['#FE0000', '#000095'] }
  },
  {
    code: 'SW',
    nativeName: 'Kiswahili',
    name: 'Swahili',
    region: 'East Africa • Nairobi',
    flag: 'KE',
    flagSpec: { type: 'h3', colors: ['#000000', '#BB0000', '#006600'] }
  },
  {
    code: 'AF',
    nativeName: 'Afrikaans',
    name: 'Afrikaans',
    region: 'South Africa • Johannesburg',
    flag: 'ZA',
    flagSpec: { type: 'h3', colors: ['#E03C31', '#007749', '#001489'] }
  }
];

/**
 * Renderizador vectorial universal de las 56 banderas (estilo quantlambda.dev),
 * garantizando nitidez en Linux, macOS y Windows sin depender de fuentes emoji.
 */
export function FlagBadge({ lang, width = 20, height = 14 }) {
  const spec = lang?.flagSpec || { type: 'h3', colors: ['#AA151B', '#F1BF00', '#AA151B'] };
  const [c1, c2, c3] = spec.colors;
  const baseStyle = {
    borderRadius: '3px',
    overflow: 'hidden',
    flexShrink: 0,
    boxShadow: '0 0 0 1px rgba(148, 163, 184, 0.32)',
    display: 'inline-block'
  };

  if (spec.type === 'br') {
    return (
      <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
        <rect width="24" height="16" fill={c1} />
        <polygon points="12,2.2 21.5,8 12,13.8 2.5,8" fill={c2} />
        <circle cx="12" cy="8" r="3.3" fill={c3} />
      </svg>
    );
  }
  if (spec.type === 'v3') {
    return (
      <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
        <rect width="8" height="16" fill={c1} />
        <rect x="8" width="8" height="16" fill={c2} />
        <rect x="16" width="8" height="16" fill={c3} />
      </svg>
    );
  }
  if (spec.type === 'h3') {
    return (
      <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
        <rect width="24" height="5.34" fill={c1} />
        <rect y="5.33" width="24" height="5.34" fill={c2} />
        <rect y="10.66" width="24" height="5.34" fill={c3} />
      </svg>
    );
  }
  if (spec.type === 'h2') {
    return (
      <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
        <rect width="24" height="8" fill={c1} />
        <rect y="8" width="24" height="8" fill={c2} />
      </svg>
    );
  }
  if (spec.type === 'cross') {
    return (
      <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
        <rect width="24" height="16" fill={c1} />
        <rect x="7" width="3.2" height="16" fill={c2} />
        <rect y="6.4" width="24" height="3.2" fill={c2} />
      </svg>
    );
  }
  if (spec.type === 'circle') {
    return (
      <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
        <rect width="24" height="16" fill={c1} />
        <circle cx="12" cy="8" r="4.3" fill={c2} />
      </svg>
    );
  }

  return (
    <svg width={width} height={height} viewBox="0 0 24 16" style={baseStyle} aria-hidden="true">
      <rect width="24" height="16" fill="#B22234" />
      <rect y="2.3" width="24" height="2.2" fill="#FFFFFF" />
      <rect y="6.8" width="24" height="2.2" fill="#FFFFFF" />
      <rect y="11.3" width="24" height="2.2" fill="#FFFFFF" />
      <rect width="10.5" height="8.8" fill="#3C3B6E" />
      <circle cx="3" cy="2.5" r="0.7" fill="#FFFFFF" />
      <circle cx="5.5" cy="2.5" r="0.7" fill="#FFFFFF" />
      <circle cx="8" cy="2.5" r="0.7" fill="#FFFFFF" />
      <circle cx="4.2" cy="4.5" r="0.7" fill="#FFFFFF" />
      <circle cx="6.8" cy="4.5" r="0.7" fill="#FFFFFF" />
      <circle cx="3" cy="6.5" r="0.7" fill="#FFFFFF" />
      <circle cx="5.5" cy="6.5" r="0.7" fill="#FFFFFF" />
      <circle cx="8" cy="6.5" r="0.7" fill="#FFFFFF" />
    </svg>
  );
}
