import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ReservationCalendar from '../components/ReservationCalendar';

describe('ReservationCalendar', () => {
    it('予約データがない場合にメッセージを表示する', () => {
        // 1. 最初に失敗するテストを書く (Red)
        render(<ReservationCalendar reservations={[]} />);
        expect(screen.getByText('予約はありません。')).toBeInTheDocument();
    });

    it('予約データをリスト表示する', () => {
        const mockReservations = [
            { id: 1, resource_id: 'A', start_time: '...', user_name: 'User A' },
        ];
        render(<ReservationCalendar reservations={mockReservations} />);
        expect(screen.getByText('User A')).toBeInTheDocument();
    });
});
