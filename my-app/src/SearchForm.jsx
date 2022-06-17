import {useState} from 'react';
import {Form} from 'react-bootstrap'
import { Switch } from '@material-ui/core';


const SearchForm = (props) => {
    const [query, setQuery] = useState(props.data);
    const [svd_k, setSvd_k] = useState(props.svd_k);

    const handleSubmit = (event) => {
        event.preventDefault()
        props.handler({
            "query": query,
            "svd_k": svd_k
        });
    };

    const changeQuery = (e) => {
        setQuery(e.target.value);
    }

    const changeSVD = (e) => {
        setSvd_k(!svd_k);
    }

    // i think i don't need that
    const refreshPage = () => {
        window.location.reload();
    }

    return (
        <div>
            <Form onSubmit={handleSubmit}>
                <label>
                        Search:
                    <input type="text" value={query} onChange={changeQuery} />
                </label>
                <label>
                    <input
                    type="checkbox"
                    checked={svd_k}
                    onChange={changeSVD}
                    />
                    SVD
                </label>
                <input type="submit" value="Wyślij" />
            </Form>
        </div>
    )
}

export default SearchForm;