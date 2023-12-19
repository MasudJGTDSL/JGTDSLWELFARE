function HeaderChange(a, b) {
    return (document.getElementById("head01").innerHTML = a, 
    document.getElementById("head02").innerHTML = b);
}
const url = '/pmis/Details/'
const searchForm = document.getElementById('searchForm')
const Input=document.getElementById("searchInput")
const resultsBox = document.getElementById('results-box') 
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const sendSearchData=(search)=>{ 
    $.ajax({
        type: 'POST', 
        url: '', 
        data: {
        'csrfmiddlewaretoken': csrf, 
        'search': search,
        },
        success: (res)=>{
            const data = res.data 
            if(Array.isArray(data)){
                resultsBox.innerHTML = ""
                data.forEach(search=>{
                resultsBox.innerHTML += `
                <a href="${url}${search.pk}" class="item">
                <div class="row mt-2 mb-2">
                <div class="col-2">
                <img src="${search.image}" class="search-img"> </div>
                <div class="col-10">
                <h5>${search.name}</h5>
                <p class="text-muted">${search.designation}</p> </div>
                </div>
                </a>
                `
                })
            }else{
            if(Input.value.length>0){
            resultsBox.innerHTML = `<b>${data}</b>`
            }else{
                resultsBox.classList.add('not-visible')
            }
        }
                },
        error: (err)=>{
        console.log(err)
                }
    })
}

Input.addEventListener("keyup", e=>{
    if (resultsBox.classList.contains('not-visible')){
        resultsBox.classList.remove('not-visible')
        }
    sendSearchData(e.target.value)
})

