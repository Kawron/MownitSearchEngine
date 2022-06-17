import logo from './logo.svg';
import './App.css';
import {useState} from 'react'
import SearchForm from './SearchForm';
import SearchResults from './SearchResults';

function App() {
  const [query, setQuery] = useState("")
  const [displayRes, setDisplayRes] = useState(false)
  const [svd_k, setSvd_k] = useState(false)
  const [searchRes, setSearchRes] = useState([])

  const handler = (input) => {
    setQuery(input.query)
    setSvd_k(input.svd_k)
    searchQuery(input)
  }

  const searchQuery = (query) => {
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(query)
    };
    fetch('/search', requestOptions)
        .then(response => response.json())
        .then((data) => {setSearchRes(data.result);
              setDisplayRes(true)});
  }

  return (
    <div className="App">
      {(displayRes) ? 
      <div> 
        <p>dupa</p>
        <SearchForm handler={handler} data={query} svdVal={svd_k}/>
        <SearchResults data={searchRes}/>
      </div>
       : 
      <div> 
        <p>dupa</p>
        <SearchForm handler={handler} data={query} svdVal={svd_k}/>
      </div>
      }
    </div>
  );
}

export default App;
