import React from 'react';

const ResourceList = ({ resources }) => {
    return (
        <ul>
            {resources.map((resource, index) => (
                <li key={index}>{resource.name}</li>
            ))}
        </ul>
    );
};

export default ResourceList;
