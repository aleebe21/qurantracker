from flask import Flask, render_template, request

app = Flask(__name__)

CHAPTERS = {
    1: "Al-Fatihah", 2: "Al-Baqarah", 3: "Aal-e-Imran", 4: "An-Nisa", 5: "Al-Ma'idah",
    6: "Al-An'am", 7: "Al-A'raf", 8: "Al-Anfal", 9: "At-Tawbah", 10: "Yunus",
    11: "Hud", 12: "Yusuf", 13: "Ar-Ra'd", 14: "Ibrahim", 15: "Al-Hijr",
    16: "An-Nahl", 17: "Al-Isra", 18: "Al-Kahf", 19: "Maryam", 20: "Ta-Ha",
    21: "Al-Anbiya", 22: "Al-Hajj", 23: "Al-Mu'minun", 24: "An-Nur", 25: "Al-Furqan",
    26: "Ash-Shu'ara", 27: "An-Naml", 28: "Al-Qasas", 29: "Al-Ankabut", 30: "Ar-Rum",
    31: "Luqman", 32: "As-Sajdah", 33: "Al-Ahzab", 34: "Saba", 35: "Fatir",
    36: "Ya-Sin", 37: "As-Saffat", 38: "Sad", 39: "Az-Zumar", 40: "Ghafir",
    41: "Fussilat", 42: "Ash-Shura", 43: "Az-Zukhruf", 44: "Ad-Dukhan", 45: "Al-Jathiyah",
    46: "Al-Ahqaf", 47: "Muhammad", 48: "Al-Fath", 49: "Al-Hujurat", 50: "Qaf",
    51: "Adh-Dhariyat", 52: "At-Tur", 53: "An-Najm", 54: "Al-Qamar", 55: "Ar-Rahman",
    56: "Al-Waqi'ah", 57: "Al-Hadid", 58: "Al-Mujadila", 59: "Al-Hashr", 60: "Al-Mumtahanah", 61: "As-Saff", 62: "Al-Jumu'ah",
    63: "Al-Munafiqun", 64: "At-Taghabun", 65: "At-Talaq", 66: "At-Tahrim", 67: "Al-Mulk",
    68: "Al-Qalam", 69: "Al-Haqqah", 70: "Al-Ma'arij", 71: "Nuh", 72: "Al-Jinn",
    73: "Al-Muzzammil", 74: "Al-Muddaththir", 75: "Al-Qiyamah", 76: "Al-Insan", 77: "Al-Mursalat",
    78: "An-Naba", 79: "An-Nazi'at", 80: "Abasa", 81: "At-Takwir", 82: "Al-Infitar",
    83: "Al-Mutaffifin", 84: "Al-Inshiqaq", 85: "Al-Buruj", 86: "At-Tariq", 87: "Al-A'la",
    88: "Al-Ghashiyah", 89: "Al-Fajr", 90: "Al-Balad", 91: "Ash-Shams", 92: "Al-Lail",
    93: "Ad-Duha", 94: "Ash-Sharh", 95: "At-Tin", 96: "Al-Alaq", 97: "Al-Qadr",
    98: "Al-Bayyinah", 99: "Az-Zalzalah", 100: "Al-Adiyat", 101: "Al-Qari'ah", 102: "At-Takathur",
    103: "Al-Asr", 104: "Al-Humazah", 105: "Al-Fil", 106: "Quraish", 107: "Al-Ma'un",
    108: "Al-Kawthar", 109: "Al-Kafirun", 110: "An-Nasr", 111: "Al-Masad", 112: "Al-Ikhlas",
    113: "Al-Falaq", 114: "An-Nas"
}

class QuranTracker:
    def __init__(self):
        self.verse_counts = {1:7, 2:286, 3:200, 4:176, 5:120, 6:165, 7:206, 8:75, 9:129, 10:109, 11:123, 12:111, 13:43, 14:52, 15:99, 16:128, 17:111, 18:110, 19:98, 20:135, 21:112, 22:78, 23:118, 24:64, 25:77, 26:227, 27:93, 28:88, 29:69, 30:60, 31:34, 32:30, 33:73, 34:54, 35:45, 36:83, 37:182, 38:88, 39:75, 40:85, 41:54, 42:53, 43:89, 44:59, 45:37, 46:35, 47:38, 48:29, 49:18, 50:45, 51:60, 52:49, 53:62, 54:55, 55:78, 56:96, 57:29, 58:22, 59:24, 60:13, 61:14, 62:11, 63:11, 64:18, 65:12, 66:12, 67:30, 68:52, 69:52, 70:44, 71:28, 72:28, 73:20, 74:56, 75:40, 76:31, 77:50, 78:40, 79:46, 80:42, 81:29, 82:19, 83:36, 84:25, 85:22, 86:17, 87:19, 88:26, 89:30, 90:20, 91:15, 92:21, 93:11, 94:8, 95:8, 96:19, 97:5, 98:8, 99:8, 100:11, 101:11, 102:8, 103:3, 104:9, 105:5, 106:4, 107:7, 108:3, 109:6, 110:3, 111:5, 112:4, 113:5, 114:6}
        self.total = sum(self.verse_counts.values())
        self.current = 0

    def update(self, chapter, verse):
        self.current = sum(self.verse_counts[i] for i in range(1, chapter)) + verse
        return f"{self.current/self.total:.1%} complete"

    def plan(self, days):
        verses_per_day = (self.total - self.current) / days
        target_verse = self.current + verses_per_day
        target_chapter = 1
        verse_count = 0
        for chapter, verses in self.verse_counts.items():
            verse_count += verses
            if verse_count > target_verse:
                target_chapter = chapter
                target_verse = int(target_verse - (verse_count - verses))
                break

        return f"Read {verses_per_day:.1f} verses daily. Stop at Surah {target_chapter} ({CHAPTERS[target_chapter]}), Verse {target_verse}"

@app.route('/', methods=['GET', 'POST'])
def index():
    tracker = QuranTracker()
    progress = None
    plan = None
    if request.method == 'POST':
        chapter = int(request.form['chapter'])
        verse = int(request.form['verse'])
        days = int(request.form['days'])
        progress = tracker.update(chapter, verse)
        plan = tracker.plan(days)
    return render_template('index.html', chapters=CHAPTERS, progress=progress, plan=plan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)