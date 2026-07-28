---
title: Bagaimana cara menggunakan OWASP Top 10 sebagai sebuah standarisasi
source: owasp.org
url: https://owasp.org/Top10/2021/id/A00_2021_How_to_use_the_OWASP_Top_10_as_a_standard/
collector: owasp
category: web-security
tags:
- web-security
- owasp
- top
- yang
- sebuah
date_collected: '2026-07-25T14:27:15.908699Z'
language: unknown
---

# Bagaimana cara menggunakan OWASP Top 10 sebagai sebuah standarisasi

OWASP Top 10 terutama merupakan dokumen kesadaran. Bagaimanapun, hal ini tidak menutup organisasi untuk menggunakannya sebagai sebuah standar de facto pada industri keamanan aplikasi sejak kelahirannya pada tahun 2003. Apabila anda ingin menggunakan OWASP Top 10 sebagai standar dalam coding atau pengujian, ketahuilah bahwa ini adalah batas minimal dan hanya sebuah tahap awal.

Salah satu kesulitan dalam menggunakan OWASP Top 10 sebagai sebuah standar adalah kita mendokumentasikan resiko keamanan aplikasi, dan belum tentu sebuah masalah yang mudah diuji. Sebagai contohnya, A04:2021-Insecure Design yang mana berada di luar cakupan sebagian besar bentuk dari pengujian. Contoh lainnya adalah pengujian di tempat, digunakan, dan pencatatan dan pemantauan yang efektif hanya dapat dilakukan dengan wawancara dan meminta sebuah sampel dari respon tanggapan insiden yang efektif. Sebuah alat analisa kode statis dapat melihat mengenai ketidakhadiran pada pencatatan, namun hal ini mungkin mustahil untuk ditentukan apabila business logic atau kontrol akses mencatat penjebolan keamanan yang kritis. penguji penetrasi hanya dapat menentukan bahwa mereka telah memanggil respons insiden di lingkungan pengujian, yang jarang dipantau dengan cara yang sama seperti pada produksi.

Berikut adalah rekomendasi kami mengenai kapan waktu yang tepat untuk menggunakan OWASP Top 10:

Use CaseOWASP Top 10 2021OWASP Application Security Verification StandardAwarenessYesTrainingEntry levelComprehensiveDesign and architectureOccasionallyYesCoding standardBare minimumYesSecure Code reviewBare minimumYesPeer review checklistBare minimumYesUnit testingOccasionallyYesIntegration testingOccasionallyYesPenetration testingBare minimumYesTool supportBare minimumYesSecure Supply ChainOccasionallyYes

Kami akan mendorong siapa pun yang ingin mengadopsi standar keamanan aplikasi untuk menggunakan OWASP Application Security Verification Standar (ASVS), yang mana ini dirancang agar dapat diverifikasi dan diuji, dan dapat digunakan di berbagai bagian dari siklus hidup pengembangan yang aman.

ASVS hanyalah sebuah pilihan yang dapat diterima untuk vendor alat. Alat tidak bisa secara menyeluruh mendeteksi, menguji, ataupun melindungi dari OWASP Top 10 dikarenakan sifat dari beberapa resiko OWASP Top 10, dengan mengacu kepada A04:2021-Insecure Design. OWASP tidak menyarankan penangguhan penuh dari OWASP Top 10, dikarenakan hal itu tidak benar.
