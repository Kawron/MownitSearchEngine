import {Container, Row} from 'react-bootstrap'

const SearchResults = (props) => {
    return (
        <Container>
            {props.data.map(object => {
                return (
                    <Row>
                        <div> {object.url} </div>
                        <div><a href={object.url}> {object.title} </a></div>
                    </Row>
                )
            })}
        </Container>
    );
}

export default SearchResults;