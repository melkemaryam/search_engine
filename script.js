
let abc

document.getElementById("search-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    // Clear previous search results
    document.getElementById("results_container").innerHTML = " ";


    const query = document.getElementById("search-input").value;
    const algorithm = document.querySelector('input[name="algorithm"]:checked').value;
    const response = await fetch(`http://127.0.0.1:8000/search?query=${query}&algorithm=${algorithm}`);
    const responseText = await response.json();
  
    const jsonString = '[' + responseText.replace(/}{/g, '},{') + ']';
    const data = JSON.parse(jsonString);
    console.log(data);
    displayResults(data[0]);
    abc = data[0];
  });

inner_html = ''

results_container = document.getElementById('results_container')

//looping through abc to fill the html_template
displayResults = (abc) => {
    let inner_html = '';

    for (let i = 0; i < abc.length; i++) {
        let inner_data = abc[i];
        let rank = inner_data.rank;
        let url = inner_data.url;
        let doc_id = inner_data.doc_id;
        let snippet = inner_data.text;

        html_template = `
            <div class="sub_results">
                <div class="rank_header">
                    <h3>rank: ${rank} </h3>
                    <span>
                        <select class="rank_dropdown" aria-label="label for the select">
                            <option value="0">0</option>
                            <option value="1">1</option>
                            <option value="2">2</option>
                        </select>
                    </span>
                </div>
                <h4><a href="${url}" target="_blank">${url}</a></h4>
                <p>
                    ${snippet}
                </p>
            </div>
            `;
        inner_html += html_template;
    }
    results_container.innerHTML = inner_html;
};



//decorations
document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.rank_dropdown');

    dropdowns.forEach((dropdown) => {
        dropdown.addEventListener('change', () => {
            console.log(`Selected value: ${dropdown.value}`);
        });
    });
});


//
document.getElementById("reset-button").addEventListener("click", () => {
    document.getElementById("search-input").value = "";
    document.getElementById("results_container").innerHTML = "";
  });
  
  document.getElementById("send-button").addEventListener("click", () => {
    // Add your code for the "Send" button here
  });
  

  document.getElementById("search-input").addEventListener("focus", () => {
    document.getElementById("search-input").style.maxWidth = "100%";
  });
  
  document.getElementById("search-input").addEventListener("blur", () => {
    document.getElementById("search-input").style.maxWidth = "600px";
  });
  