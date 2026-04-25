# Writeup

jadi disini gw bakal ngerjain ulang soal ret2libc via format strings tanpa adanya ai

![Gambar](../assets/1/1.1.png)

kalo dilihat pake checsec kelihatan kalo gak ada canary tapi PIE nya enabled dan kalo PIE nya enabled biasanya ASLR juga ada

Dari source code nya kelihatan kalo printf di function helper rentan sama format strings tepatnya di line ke 13, dan scanf di function main rentan sama buffer overflow, kelihatan kalo disitu gak dikasih batesan size nya

jadi disini karena printf nya rentan karena gak dikasih formatnya, kalo dicoba dengan %p ini bakal leak RDI nya dan karena ini leak RDI berarti yang keleak itu Calling Convention kayak RDI RSI RDX R8 R9 dan kalo udah lebih dari itu? 

kalo lebih dari itu bakal masuk ke stack yang berarti bisa leak segala macam hal bahkan libc target utama gw

![Gambar](../assets/1/1.2.png)

pertama gw coba break di helper+97 tempat dimana rentan format strings lalu gw run

![Gambar](../assets/1/1.3.png)

setelahnya gw coba cek di stack dan benar aja ada libc nya tepatnya di urutan ke 21, darimana 21? stack mulai jika sudah lebih dari Calling Convention yang berarti mulai dari ke 6

![Gambar](../assets/1/1.4.png)

selanjutnya gw coba leak dan berhasil bahkan sudah dapat offsetnya juga, sisanya gw tinggal mencari gadget, ret, binsh dan system juga offset buffer nya

![Gambar](../assets/1/1.5.png)

sekarang gw coba jalanin dan harusnya berhasil tapi ternyata gw gagal, pas gw cek pake ldd ternyata libc.so.6 yang dipake salah, habis itu cuma gw benerin dengan patch

![Gambar](../assets/1/1.6.png)

dan sudah benar sekarang, tapi masalahnya satu offsetnya pasti berbeda jadi gw coba ulang buat dapetin offset dari leaknya ke base

![Gambar](../assets/1/1.7.png)

offset dari leak ke base udah dapet sisanya ya ubah pake offset yang baru dan jalanin pake script yang sama 

![Gambar](../assets/1/1.8.png)

dan ya gw berhasil dapetin shell nya

---

## Lesson Learned
- jangan lupa cek file nya pake ldd dan sesuainkan dengan yang benar
