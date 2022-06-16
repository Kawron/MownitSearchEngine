import {Container, Row} from 'react-bootstrap'
import './SearchResult.css';

const SearchResult = (props) => {
    return (
        <Container>
            {props.data.map((object, i) => {
                return (
                    <Row className="result-row">
                        <div className="result-url"> {object.url} </div>
                        <div className="result-title"><a href={object.url}> {object.title} </a></div>
                        <div className="result-text"> {object.short_text} [...] </div>
                    </Row>
                )
            })}
        </Container>
    );
}

export default SearchResult;