const ReservationCalendar = ({ reservations }) => {
    if (!reservations || reservations.length === 0) {
        return <p>予約はありません。</p>;
    }

    return (
        <ul>
            {reservations.map((res) => (
                <li key={res.id}>{/* 予約情報を表示 */}</li>
            ))}
        </ul>
    );
};

export default ReservationCalendar;
