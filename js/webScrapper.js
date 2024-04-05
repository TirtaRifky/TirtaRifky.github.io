$(function(){
    //Mengambil data dari file Scrapped.json menggunakan fungsi $.getJSON() JQuery
    $.get('Scrapped.json',function(obj){
        //Tag tabel awal
        var str="<table border='1'>";
        //Judul tabel
        str+="<tr><td>No</td><td>Judul</td><td>Kategori</td><td>Waktu Publish</td><td>Waktu Scrapping</td></tr>";
        //Looping data dari objek JSON dengan fungsi $.each() JQuery
        $.each(obj,function(n,data){
            //Isi tabel
            str+="<tr>";
            str+="<td>"+(n+1)+"</td>";
            str+="<td>"+data.Judul+"</td>";
            str+="<td>"+data.Kategori+"</td>";
            str+="<td>"+data['Waktu Publish']+"</td>";
            str+="<td>"+data['Waktu Scrapping']+"</td>";
            str+="</tr>";
        });
        //Tag tabel penutup
        str+="</table>";
        //Menampilkan semua data ke dalam tabel HTML dengan id="scrapped_json"
        $('#scrapped_json').html(str);
    });
});