import {useState} from 'react';
import {Container, Row, Col, Form, Button} from 'react-bootstrap'

const SearchForm = (props) => {
    const [text, setText] = useState(props.data);
    const [lowRankApprox, setLowRankApprox] = useState(props.lowRankApprox);

    const handleSubmit = (event) => {
        event.preventDefault()
        props.handler({
            "search_query": text,
            "low_rank_approx": lowRankApprox //change to svd_k
        });
    };

    return (
        <Form onSubmit={handleSubmit}>

            <Form.Group className="mb-3" controlId="formText">
                <Form.Control
                    type="text"
                    placeholder=""
                    value={text}
                    onChange={e => setText(e.target.value)}
                />
            </Form.Group>

            <Container>
                <Row className="justify-content-center align-items-center">
                    <Col xs="12" lg="6">
                        <Form.Check
                            type="switch"
                            label="Low rank approx."
                            checked={lowRankApprox}
                            onChange={() => setLowRankApprox(!lowRankApprox)}
                        />
                    </Col>
                    <Col xs="12" lg="1" style={{height: "10px"}}>
                    </Col>
                    <Col xs="12" lg="5">
                        <Button className="w-100" variant="outline-primary" type="submit">
                            Search
                        </Button>
                    </Col>
                </Row>
            </Container>
        </Form>
    )
}

export default SearchForm;