import {useState} from 'react';
import './App.css';
import SearchForm from './SearchForm.js'
import SearchResult from './SearchResult.js'
import {Container, Row, Col} from 'react-bootstrap'

function App() {
  const [view, setView] = useState(0);
  const [searchQuery, setSearchQuery] = useState("")
  const [lowRankApprox, setLowRankApprox] = useState(false)
  const [searchResult, setSearchResult] = useState([])

  const handler = (inputData) => {
      setSearchQuery(inputData.search_query)
      setLowRankApprox(inputData.low_rank_approx)
      console.log(inputData)
      sendQuery(inputData)
  }

  const sendQuery = (values) => {
      const requestOptions = {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify(values)
      };

      fetch('/search_query', requestOptions)
          .then((response) => {
              response.json()
                  .then((data) => {
                      console.log(data.result);
                      setSearchResult(data.result)
                      setView(1)
                  });
          });
  }

  return (
        <div className="App">
          <p>DUPA</p>
            {(view === 0) ?
                <div className="jumbotron d-flex align-items-center min-vh-100">
                    <Container className="centred-browser-from-wrapper">
                        <Row className="justify-content-center">
                            <Col xs="6">
                                <SearchForm handler={handler} data={searchQuery} lowRankApprox={lowRankApprox} inline={false}/>
                            </Col>
                        </Row>
                    </Container>

                </div>
                :
                <Container className="centred-browser-from-wrapper">
                    <Row className="justify-content-center">
                        <Col xs="10">
                            <SearchForm handler={handler} data={searchQuery} lowRankApprox={lowRankApprox} inline={true}/>
                        </Col>
                    </Row>
                    <Row className="justify-content-center">
                        <Col xs="12" md="10" lg="7">
                            <SearchResult data={searchResult}/>
                        </Col>
                    </Row>
                </Container>
            }
        </div>
    );
}

export default App;
