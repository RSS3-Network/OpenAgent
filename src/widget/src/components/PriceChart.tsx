/* eslint-disable no-console */
function getQueryParams() {
    const params = new URLSearchParams(window.location.search);
    return {
        token: params.get('token') || 'btc',

    };
}

export function PriceChart() {
    const {
        token
    } = getQueryParams();

    return (
        <>
            <div>
                <gecko-coin-price-chart-widget locale="en" outlined="true" coin-id={token}
                                               initial-currency="usd"></gecko-coin-price-chart-widget>
            </div>
        </>
    );
}
