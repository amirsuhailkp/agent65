---
title: A10:2021 – Server-Side Request Forgery SSRF
source: owasp.org
url: https://owasp.org/Top10/2021/id/A10_2021-Server-Side_Request_Forgery_(SSRF)/
collector: owasp
category: web-security
tags:
- web-security
- yang
- untuk
- ssrf
- dan
date_collected: '2026-07-25T14:27:27.369051Z'
language: unknown
---

# A10:2021 – Server-Side Request Forgery (SSRF)

## Faktor-Faktor

Klasifikasi CWETingkat Kejadian MaksimumRata - Rata Tingkat KejadianCakupan MaximumRata - Rata CakupanRata - Rata Bobot ExploitasiRata - Rata Bobot DampakTotal KejadianTotal CVEs12.72%2.72%67.72%67.72%8.286.729,503385

## Penjelasan Singkat

Kategori ini ditambahkan dari survei 10 komunitas teratas (#1). Data ini menunjukan tingkat insiden yang relatif rendah dengan cakupan pengujian di atas rata-rata serta nilai dampak dan potensial eksploitasi di atas rata-rata. Entri-entri baru kemungkinan besar menjadi cluster kecil atau tunggal dari CWE - CWE karena tingkat atensi dan tingkat kesadarannya, harapannnya entri-entri baru ini dapat menjadi fokusan riset keamanan dan dapat digolongkan/dimasukkan kedalam kategori/cluster yang lebih besar di edisi mendatang.

## Deskripsi

Kecacatan *SSRF* muncul saat sebuah aplikasi web meminta *remote resource* tanpa melakukan validasi URL yang di berikan oleh pengguna. Ini memperbolehkan penyerang untuk memaksa aplikasi untuk mengirim *crafted request* ke destinasi yang tidak diharapkan, meskipun sudah dilindungi oleh *firewall*, VPN, atau tipe lain dari daftar aturan akses jaringan - *Access Control List* (ACL).

Aplikasi web saat ini menyediakan fitur yang nyaman bagi pengguna akhir, sehingga proses meminta URL menjadi hal yang lumrah. Oleh karena itu, insiden *SSRF* semakin meningkat. Selain itu, tingkat keparahan *SSRF* semakin meningkat karena layanan-layanan *cloud* dan tingkat komplexitas arsitektur *cloud*.

## Bagaimana Cara Mencegahnya

Pengembang dapat mencegah terjadinya *SSRF* dengan mengimplementasikan beberapa atau semua tindakan kontrol pertahanan berikut:

### Dari Network Layer

- Segmentasi fitur/fungsi *remote resource access*di jaringan yang berbeda untuk mengurangi dampak dari*SSRF*.
- Terapkan kebijakan firewall *deny by default*atau aturan kontrol akses jaringan untuk memblokir semua lalu lintas eksternal kecuali lalu lintas intranet yang penting.
  *Petunjuk:*
  ~ Buat / Bangunlah siklus hidup dan hak kepemilikan untuk peraturan firewall berdasarkan aplikasinya.
  ~ Catat semua akses jaringan yang melewati firewall baik akses jaringan yang diterima ataupun yang diblokir/tolak (lihat[A09:2021-Security Logging and Monitoring Failures](../A09_2021-Security_Logging_and_Monitoring_Failures/)).

### Dari Application Layer

- Bersihkan dan validasi semua data inputan yang dimasukkan oleh klien
- Terapkan skema URL, port, dan destinasi dengan daftar izin positif
- Jangan mengirim respon mentah ke klien
- Nonaktifkan pengalihan HTTP
- Perhatikan konsistensi URL untuk menghindari serangan

  *DNS rebinding*dan serangan*(TOCTOU) time of check, time of use*

Jangan gunakan daftar penolakan atau ekspresi reguler untuk mitigasi *SSRF*. Penyerang mempunyai daftar muatan, alat, dan kemampuan untuk membobol/melewati daftar penolakan.

### Tindakan Lainnya Yang Dapat Dipertimbangkan

- Jangan

  *deploy*layanan yang berhubungan dengan keamanan pada sistem yang berada di barisan depan, contohnya*OpenId*. Kontrol lalu lintas lokal pada sistem ini (Localhost).
- Khusus untuk

  *frontends*dengan pengguna/grup pengguna yang loyal atau berdedikasi serta dapat dikelola gunakanlah enkripsi jaringan (VPN) pada sistem independen mengingat adanya kebutuhan proteksi yang sangat tinggi.

## Contoh Skenario Penyerangan

Penyerang dapat menggunakan *SSRF* untuk menyerang sitem yang telah dilindungi dibalik firewall aplikasi web, firewall,atau jaringan ACL dengan skenario-skenario penyerangan sebagai berikut:

**Skenario #1:** Memindai port server internal. Apabila arsitektur jaringan tidak tersegmentasi, penyerang dapat mendapatkan gambaran bagaimana jaringan internal terbentuk
dan dapat menentukan port-port mana yang terbuka atau tertutup pada server internal berdasarkan hasil koneksi, waktu yang dibutuhkan untuk melakukan koneksi atau waktu yang dibutuhkan untuk menolak koneksi yang bermuatan *SSRF*.

**Skenario #2:** Kebocoran data sensitif. Penyerang dapat mengakses file lokal seperti
```
file:///etc/passwd</span>
```

dan
```
http://localhost:28017/
```

.

**Skenario #3:** Akses penyimpanan metadata dari layanan cloud - Mayoritas penyedia layanan cloud memiliki penyimpanan metadata seperti
```
http://169/254.169.254/
```

.
Seorang penyerang dapat membaca metada tersebut untuk mendapatkan informasi sensitif.

**Skenario #4:** Penyusupan layanan internal - Penyerang dapat menyalahgunakan layanan internal untuk melakukan serangan lebih lanjut seperti *Remote Code Execution (RCE)* atau *Denial Of Service (DOS)*.
