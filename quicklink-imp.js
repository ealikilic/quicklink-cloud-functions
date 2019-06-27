<script  async defer src="https://unpkg.com/quicklink@1.0.0/dist/quicklink.umd.js"></script>
<script language="javascript">
window.addEventListener('load', () =>{
	let host = window.location.origin;
	let regex = new RegExp("https:\/\/www.+..\.(..)");
	let base = regex.exec(host);
	let storageurl = "//storage.googleapis.com/quicklink-resource-lists/ql-res-list-"+base[1]+".json"; 
	let reslist;
	fetch(storageurl,{credentials:'same-origin'})
		.then(res => res.json())
		.then((out) => {
			quicklink({urls:out});
		})
		.catch(err => { throw err });
});
</script>
